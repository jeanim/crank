import pymel.core as pm
import maya.cmds as cmds
from pymel import versions
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from mgear.vendor.Qt import QtCore, QtWidgets, QtGui
from mgear.core import transform, node, attribute, applyop, pyqt, utils, curve
from mgear.core import string

from . import crankUI

'''
TODO:

    layer lister:
        -Right click menu
            -Select members
            -Toggle ON/OFF
            -Solo
            -Random Color (for each object in the layer)
            -Ghost Create
            -Ghost Delete
            -Delete Selected Layer
            -----------
            -Add selected to layer
            -Remove selected from layer
            -----------
            -Turn Selected ON
            -Turn Selected OFF
            -----------
            -Turn All ON
            -Turn All OFF


    sculpt frame attributes:
        -frame number

    call back to exit edit mode if frame change

'''

####################################
# Crank
####################################

CRANK_TAG = "_isCrankLayer"

####################################
# Layer Node
####################################


def create_layer(oSel):

    oSel = [x for x in oSel
            if x.getShapes()
            and x.getShapes()[0].type() == 'mesh']

    if oSel:
        result = pm.promptDialog(title='Crank Layer Name',
                                 message='Enter Name:',
                                 button=['OK', 'Cancel'],
                                 defaultButton='OK',
                                 cancelButton='Cancel',
                                 dismissString='Cancel',
                                 text="")

        if result == 'OK':
            text = pm.promptDialog(query=True, text=True)
            name = string.normalize(text)

            layer_node = create_layer_node(name, oSel)
            bs_list = create_blendshape_node(name, oSel)
            for bs in bs_list:
                layer_node.crank_layer_envelope >> bs.envelope
                idx = attribute.get_next_available_index(
                    layer_node.layer_blendshape_node)
                pm.connectAttr(bs.message,
                               layer_node.layer_blendshape_node[idx])
            pm.select(oSel)

            return layer_node


def create_blendshape_node(bsName, oSel):
    bs_list = []
    for obj in oSel:
        bs = pm.blendShape(obj,
                           name="_".join([obj.name(),
                                          bsName,
                                          "blendShape_crank"]),
                           foc=False)[0]
        bs_list.append(bs)

    return bs_list


def create_layer_node(name, affectedElements):
        # create a transform node that contain the layer information and

    fullName = name + "_crankLayer"

    # create node
    if pm.ls(fullName):
        pm.displayWarning("{} already exist".format(fullName))
        return
    layer_node = pm.createNode("transform",
                               n=fullName,
                               p=None,
                               ss=True)
    attribute.lockAttribute(layer_node)
    # add attrs
    attribute.addAttribute(
        layer_node, CRANK_TAG, "bool", False, keyable=False)
    # affected objects
    layer_node.addAttr("layer_objects", at='message', m=True)
    layer_node.addAttr("layer_blendshape_node", at='message', m=True)
    # master envelope for on/off
    attribute.addAttribute(layer_node,
                           "crank_layer_envelope",
                           "float",
                           value=1,
                           minValue=0,
                           maxValue=1)
    # create the post-blendshapes nodes for each affected object

    # connections
    for x in affectedElements:
        idx = attribute.get_next_available_index(layer_node.layer_objects)
        pm.connectAttr(x.message, layer_node.layer_objects[idx])

    return layer_node


def list_crank_layer_nodes():
    return [sm for sm in cmds.ls(type="transform") if cmds.attributeQuery(
        CRANK_TAG, node=sm, exists=True)]


def get_layer_affected_elements(layer_node):
    if not isinstance(layer_node, list):
        layer_node = [layer_node]
    members = []
    for lyr in layer_node:
        members = members + lyr.layer_objects.inputs()
    return set(members)


####################################
# sculpt frame
####################################

def add_frame_sculpt(layer_node, anim=False, keyf=[1, 0, 0, 1], solo=False):

    objs = layer_node.layer_objects.inputs()
    bs_node = layer_node.layer_blendshape_node.inputs()

    # ensure other targets are set to false the edit flag

    # get current frame
    cframe = int(pm.currentTime(query=True))

    # get valid name. Check if frame is ducplicated in layer
    frame_name = "frame_{}".format(str(cframe))
    i = 1
    while layer_node.hasAttr(frame_name):
        frame_name = "frame_{}_v{}".format(str(cframe), str(i))
        i += 1

    # create frame master channel
    master_chn = attribute.addAttribute(layer_node,
                                        frame_name,
                                        "float",
                                        value=1,
                                        minValue=0,
                                        maxValue=1)

    # keyframe in range the master channel
    if anim:
        # current frame
        pm.setKeyframe(master_chn,
                       t=[cframe],
                       v=1,
                       inTangentType="linear",
                       outTangentType="linear")

        # pre and post hold
        pre_hold = keyf[1]
        if pre_hold:
            pm.setKeyframe(master_chn,
                           t=[cframe - pre_hold],
                           v=1,
                           inTangentType="linear",
                           outTangentType="linear")

        post_hold = keyf[2]
        if post_hold:
            pm.setKeyframe(master_chn,
                           t=[cframe + post_hold],
                           v=1,
                           inTangentType="linear",
                           outTangentType="linear")

        # ease in and out
        if keyf[0]:
            ei = pre_hold + keyf[0]
            pm.setKeyframe(master_chn,
                           t=[cframe - ei],
                           v=0,
                           inTangentType="linear",
                           outTangentType="linear")
        if keyf[3]:
            eo = post_hold + keyf[3]
            pm.setKeyframe(master_chn,
                           t=[cframe + eo],
                           v=0,
                           inTangentType="linear",
                           outTangentType="linear")

    for obj, bsn in zip(objs, bs_node):
        dup = pm.duplicate(obj)[0]
        bst_name = "_".join([obj.name(), frame_name])
        pm.rename(dup, bst_name)
        indx = bsn.weight.getNumElements()
        pm.blendShape(bsn,
                      edit=True,
                      t=(obj, indx, dup, 1.0),
                      ts=True,
                      tc=True,
                      w=(indx, 1))
        pm.delete(dup)
        pm.blendShape(bsn, e=True, rtd=(0, indx))
        # is same as: bs.inputTarget[0].sculptTargetIndex.set(3)
        pm.sculptTarget(bsn, e=True, t=indx)

        # connect target to master channel
        pm.connectAttr(master_chn, bsn.attr(bst_name))


def delete_sculpt_frame():

    # delete blendshape targets

    # delete master channel

    return


def edit_sculpt_frame():
    attrs = attribute.getSelectedChannels()
    # Only one at the time!
    # we only set editable the first selected channel/frame_.
    if attrs:
        for x in pm.selected():
            if x.hasAttr(attrs[0]):
                _set_channel_edit_target(x.attr(attrs[0]), edit=True)
        return True

    else:
        pm.displayWarning("Not channels selected for edit!")
        return False


def edit_layer_off(layer_node):
    # set all targets of specific layer to edit off
    uda = layer_node.listAttr(ud=True, k=True)
    for chn in uda:
        if not chn.name().endswith("envelope"):
            _set_channel_edit_target(chn, False)


def edit_all_off():
    # set all crank layer edit off
    for lyr in list_crank_layer_nodes():
        edit_layer_off(pm.PyNode(lyr))


def _set_channel_edit_target(chn, edit=True):
    # set the blendshape target of a channel editable or not editable
    attrs = chn.listConnections(d=True, s=False, p=True)
    for a in attrs:
        if edit:
            pm.sculptTarget(a.node(), e=True, t=a.index())
            # get the time from the channel name
            pm.currentTime(int(chn.name().split(".")[-1].split("_")[1]))
            pm.inViewMessage(amg="{}: Edit mode is ON".format(chn.name()),
                             pos='midCenterBot',
                             fade=True)
        else:
            a.node().inputTarget[a.index()].sculptTargetIndex.set(-1)
            pm.mel.eval("updateBlendShapeEditHUD;")
            pm.inViewMessage(amg="{}: Edit mode is OFF".format(chn.name()),
                             pos='midCenterBot',
                             fade=True)


####################################
# Crank Tool UI
####################################

class crankUIW(QtWidgets.QDialog, crankUI.Ui_Form):

    """UI Widget
    """

    def __init__(self, parent=None):
        super(crankUIW, self).__init__(parent)
        self.setupUi(self)


class crankTool(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    valueChanged = QtCore.Signal(int)
    wi_to_destroy = []

    def __init__(self, parent=None):
        self.toolName = "Crank"
        super(crankTool, self).__init__(parent)
        self.crankUIWInst = crankUIW()

        self.__proxyModel = QtCore.QSortFilterProxyModel(self)
        self.crankUIWInst.layers_listView.setModel(self.__proxyModel)

        self.setup_crankWindow()
        self.create_layout()
        self.create_connections()
        self._refreshList()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def setup_crankWindow(self):

        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Crank: Shot Sculpting")
        self.resize(266, 445)

    def create_layout(self):

        self.crank_layout = QtWidgets.QVBoxLayout()
        self.crank_layout.addWidget(self.crankUIWInst)
        self.crank_layout.setContentsMargins(3, 3, 3, 3)

        self.setLayout(self.crank_layout)

    def setSourceModel(self, model):
        self.__proxyModel.setSourceModel(model)

    ###########################
    # Helper functions
    ###########################

    def _refreshList(self):
        model = QtGui.QStandardItemModel(self)
        for c_node in list_crank_layer_nodes():
            model.appendRow(QtGui.QStandardItem(c_node))
        self.setSourceModel(model)

    def _getSelectedListIndexes(self):
        layers = []
        for x in self.crankUIWInst.layers_listView.selectedIndexes():
            try:
                layers.append(pm.PyNode(x.data()))

            except pm.MayaNodeError:
                pm.displayWarning("{}  can't be find.".format(x.data()))
                return False
        return layers

    def select_layer_node(self):
        layers = self._getSelectedListIndexes()
        pm.select(layers)

    def create_layer(self):
        create_layer(pm.selected())
        self._refreshList()

    def add_frame_sculpt(self):
        # layer_node = pm.PyNode("ddd_crankLayer")
        anim = self.crankUIWInst.keyframe_checkBox.isChecked()
        ei = self.crankUIWInst.easeIn_spinBox.value()
        eo = self.crankUIWInst.easeOut_spinBox.value()
        pre = self.crankUIWInst.preHold_spinBox.value()
        pos = self.crankUIWInst.postHold_spinBox.value()
        for layer_node in self._getSelectedListIndexes():
            add_frame_sculpt(layer_node, anim=anim, keyf=[ei, pre, pos, eo])

        self.select_members()

    def edit_frame_sculpt(self):
        if edit_sculpt_frame():
            self.select_members()

    def edit_layer_off(self):
        for layer_node in self._getSelectedListIndexes():
            edit_layer_off(layer_node)

    def edit_all_off(self):
        edit_all_off()

    ###########################
    # "right click context menu for layers"
    ###########################

    def _layer_menu(self, QPos):

        lyr_widget = self.crankUIWInst.layers_listView
        currentSelection = lyr_widget.selectedIndexes()
        if currentSelection is None:
            return
        self.lyr_menu = QtWidgets.QMenu()
        parentPosition = lyr_widget.mapToGlobal(QtCore.QPoint(0, 0))
        menu_item_01 = self.lyr_menu.addAction("Select Members")
        self.lyr_menu.addSeparator()
        menu_item_02 = self.lyr_menu.addAction("Selected Layer Edit OFF")
        menu_item_03 = self.lyr_menu.addAction("All Layers Edit OFF")
        self.lyr_menu.addSeparator()

        menu_item_01.triggered.connect(self.select_members)
        menu_item_02.triggered.connect(self.edit_layer_off)
        menu_item_03.triggered.connect(self.edit_all_off)

        self.lyr_menu.move(parentPosition + QPos)
        self.lyr_menu.show()

    def select_members(self):
        layers = self._getSelectedListIndexes()
        pm.select(get_layer_affected_elements(layers))

    ###########################
    # create connections SIGNALS
    ###########################
    def create_connections(self):
        self.crankUIWInst.search_lineEdit.textChanged.connect(
            self.filterChanged)
        self.crankUIWInst.refresh_pushButton.clicked.connect(
            self._refreshList)
        self.crankUIWInst.createLayer_pushButton.clicked.connect(
            self.create_layer)
        self.crankUIWInst.addFrame_pushButton.clicked.connect(
            self.add_frame_sculpt)
        self.crankUIWInst.editFrame_pushButton.clicked.connect(
            self.edit_frame_sculpt)

        selModel = self.crankUIWInst.layers_listView.selectionModel()
        selModel.selectionChanged.connect(self.select_layer_node)

        # connect menu
        self.crankUIWInst.layers_listView.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.crankUIWInst.layers_listView.customContextMenuRequested.connect(
            self._layer_menu)

    #############
    # SLOTS
    #############
    def filterChanged(self, filter):
        regExp = QtCore.QRegExp(filter,
                                QtCore.Qt.CaseSensitive,
                                QtCore.QRegExp.Wildcard
                                )
        self.__proxyModel.setFilterRegExp(regExp)


def openUI(*args):
    pyqt.showDialog(crankTool)

####################################


if __name__ == "__main__":

    openUI()
