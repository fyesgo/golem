from PyQt4.QtGui import QMainWindow, QPixmap, QMessageBox

from gen.ui_RenderingMainWindow import Ui_MainWindow

from clickableqlabel import ClickableQLabel

class MainWindow( QMainWindow ):

    def closeEvent( self, event ):
        reply = QMessageBox.question(self, 'Golem Message',
            "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class RenderingMainWindow:
    ##########################
    def __init__( self ):
        self.window     = MainWindow()
        self.ui         = Ui_MainWindow()

        self.ui.setupUi( self.window )
        self.ui.previewLabel.setPixmap( QPixmap( "ui/nopreview.png" ) )

    ##########################
    def show( self ):
        self.window.show()

