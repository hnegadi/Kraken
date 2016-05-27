# Kraken_Plugin

from win32com.client import constants
import os
import sys
import inspect

from win32com.client import constants
from multiprocessing import Pool

import webbrowser

import Qt
Qt.initialize()
from Qt.QtGui import QMainWindow
from Qt.QtGui import QWidget

from PySide import QtWebKit
from PySide import QtGui, QtCore

si = Application
log = si.LogMessage

def XSILoadPlugin(in_reg):
    in_reg.Author = 'Eric Thivierge & Phil Taylor'
    in_reg.Name = 'Kraken_Plugin'
    in_reg.Major = 1
    in_reg.Minor = 0


    pluginPath = in_reg.OriginPath
    krakenDir = os.path.normpath(XSIUtils.BuildPath(pluginPath, "..", "..", "..", ".."))
    os.environ['KRAKEN_PATH'] = krakenDir
    os.environ['KRAKEN_DCC'] = 'Softimage'

    # Add the path to the module search paths so we can import the module.
    sys.path.append(os.path.join(krakenDir, 'Python' ))

    krakenExtsDir = os.path.join(krakenDir, 'Exts')
    if 'FABRIC_EXTS_PATH' not in os.environ:
        LogMessage('Unable to Load Kraken becase Fabric Engine has not be loaded.')
        return
    if krakenExtsDir not in os.environ['FABRIC_EXTS_PATH']:
        os.environ['FABRIC_EXTS_PATH'] = krakenExtsDir + os.pathsep + os.environ['FABRIC_EXTS_PATH']

    canvasPresetsDir = os.path.join(krakenDir, 'Presets', 'DFG')
    if 'FABRIC_DFG_PATH' in os.environ and canvasPresetsDir not in os.environ['FABRIC_DFG_PATH']:
        os.environ['FABRIC_DFG_PATH'] = canvasPresetsDir + os.pathsep + os.environ['FABRIC_DFG_PATH']
    else:
        os.environ['FABRIC_DFG_PATH'] = canvasPresetsDir

    krakenLoadMenu = os.getenv('KRAKEN_LOAD_MENU', 'True')
    if krakenLoadMenu == 'True':
        in_reg.RegisterMenu(constants.siMenuMainTopLevelID, "Kraken", False, False)

    in_reg.RegisterCommand('OpenKrakenEditor', 'OpenKrakenEditor')
    in_reg.RegisterCommand('KrakenBuildBipedGuide', 'KrakenBuildBipedGuide')
    in_reg.RegisterCommand('KrakenBuildBipedRig', 'KrakenBuildBipedRig')


def XSIUnloadPlugin(in_reg):
    log(in_reg.Name + ' has been unloaded.', constants.siVerbose)

    return True


def Kraken_Init(in_ctxt):

    menu = in_ctxt.source
    menu.AddCommandItem("Open UI", "OpenKrakenEditor")
    menu.AddSeparatorItem()
    menu.AddCommandItem("Build Biped Guide", "KrakenBuildBipedGuide")
    menu.AddCommandItem("Build Biped Rig", "KrakenBuildBipedRig")
    menu.AddSeparatorItem()
    menu.AddCallbackItem("Help", "OpenKrakenHelp")


# =========
# Commands
# =========
def OpenKrakenEditor_Init(in_ctxt):
    cmd = in_ctxt.Source
    cmd.Description = 'Opens the Kraken Editor'
    cmd.SetFlag(constants.siCannotBeUsedInBatch, True)
    cmd.ReturnValue = True

    return True


def OpenKrakenEditor_Execute():

    # Deffered importing: We can only import the kraken modules after the
    # plugin has loaded, as it configures the python import paths on load.
    import kraken.ui.kraken_window
    reload(kraken.ui.kraken_window)
    from kraken.ui.kraken_window import KrakenWindow
    from kraken.ui.kraken_splash import KrakenSplash

    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance(long(sianchor), QWidget)

    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    for widget in app.topLevelWidgets():
            if widget.objectName() == 'KrakenMainWindow':
                widget.showNormal()

                return

    splash = KrakenSplash(app)
    splash.show()

    window = KrakenWindow(parent=sianchor)
    window.show()

    splash.finish(window)

    return True


def KrakenBuildBipedGuide_Init(in_ctxt):
    cmd = in_ctxt.Source
    cmd.Description = 'Builds the default Kraken Biped Guide'
    cmd.ReturnValue = True

    args = cmd.Arguments

    return True


def KrakenBuildBipedGuide_Execute():

    # Deffered importing: We can only import the kraken modules after the
    # plugin has loaded, as it configures the python import paths on load.
    from kraken.core.objects.rig import Rig
    from kraken import plugins

    from kraken_examples.biped.biped_guide_rig import BipedGuideRig


    builtRig = None

    result = si.XSIInputbox("Rig Name", "Kraken: Build Biped", "Biped")
    if result != "":
        guideName = result
        guideName.replace(' ', '')
        guideName += '_guide'

        progressBar = None
        try:
            guideRig = BipedGuideRig(guideName)

            progressBar = XSIUIToolkit.ProgressBar
            progressBar.Caption = "Building Kraken Guide: " + guideRig.getName()
            progressBar.CancelEnabled = False
            progressBar.Visible = True

            builder = plugins.getBuilder()
            builtRig = builder.build(guideRig)

        finally:
            if progressBar is not None:
                progressBar.Visible = False

    else:
        log('Kraken: Build Guide Rig Cancelled!', 4)
        return False

    return builtRig


def KrakenBuildBipedRig_Init(in_ctxt):
    cmd = in_ctxt.Source
    cmd.Description = 'Builds a Kraken Rig from a .krg File'
    cmd.ReturnValue = True

    args = cmd.Arguments
    args.AddObjectArgument('bipedGuide')

    return True


def KrakenBuildBipedRig_Execute(bipedGuide):

    # Deffered importing: We can only import the kraken modules after the
    # plugin has loaded, as it configures the python import paths on load.
    from kraken.core.objects.rig import Rig
    from kraken import plugins

    from kraken_examples.biped.biped_guide_rig import BipedGuideRig

    guideName = "Biped"
    if bipedGuide == None and si.Interactive is True:
        pickGuide = si.PickElement(constants.siModelFilter, "Kraken: Pick Guide Rig", "Kraken: Pick Guide Rig")
        if pickGuide('ButtonPressed') == 0:
            pass
        else:
            pickedGuide = pickGuide('PickedElement')

            if pickedGuide.Properties('krakenRig') is None:
                log("Kraken: Picked object is not the top node of a Kraken Rig!", 4)
                return False

            guideName = pickedGuide.Name
    else:
        if bipedGuide.Properties('krakenRig') is None:
            log("Kraken: 'bipedGuide' argument is not the top node of a Kraken Rig!", 4)
            return False

        guideName = bipedGuide.Name

    guideRig = BipedGuideRig(guideName)

    synchronizer = plugins.getSynchronizer()

    if guideRig.getName().endswith('_guide') is False:
        guideRig.setName(guideRig.getName() + '_guide')

    synchronizer.setTarget(guideRig)
    synchronizer.sync()

    rigBuildData = guideRig.getRigBuildData()
    rig = Rig()
    rig.loadRigDefinition(rigBuildData)
    rig.setName(rig.getName().replace('_guide', '_rig'))

    builtRig = None
    progressBar = None
    try:

        progressBar = XSIUIToolkit.ProgressBar
        progressBar.Caption = "Building Kraken Rig: " + rig.getName()
        progressBar.CancelEnabled = False
        progressBar.Visible = True

        builder = plugins.getBuilder()
        builtRig = builder.build(rig)

    finally:
        if progressBar is not None:
            progressBar.Visible = False

    return builtRig


# ==========
# Callbacks
# ==========
def OpenKrakenHelp(in_ctxt):
    menuItem = in_ctxt.source

    webbrowser.open_new_tab('http://fabric-engine.github.io/Kraken')
