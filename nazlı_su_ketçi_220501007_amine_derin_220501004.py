import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QAction, QMenu, QGraphicsItem, \
    QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QColorDialog, QInputDialog, \
    QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QRadioButton, QLineEdit, QButtonGroup, QLabel, QCheckBox, QDockWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QTransform
from PyQt5.QtCore import Qt, QLineF, QPointF

class LogicGate(QGraphicsRectItem):
    def __init__(self, gate_type, label):
        super().__init__(0, 0, 80, 40)
        self.gate_type = gate_type
        self.label = label
        self.setBrush(QBrush(Qt.white))
        self.setPen(QPen(Qt.black, 2))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.text = QGraphicsSimpleTextItem(label, self)
        self.text.setPos(20, 10)
        self.value = None

    def contextMenuEvent(self, event):
        menu = QMenu()
        label_action = menu.addAction("Etiketi Ayarla")
        value_action = menu.addAction("Değeri Ayarla")

        action = menu.exec_(event.screenPos())

        if action == label_action:
            text, ok = QInputDialog.getText(None, "Etiketi Ayarla", "Yeni etiketi girin:")
            if ok:
                self.text.setText(text)
                self.label = text
        elif action == value_action:
            value, ok = QInputDialog.getInt(None, "Değeri Ayarla", "Değer (0 veya 1):", 0, 0, 1)
            if ok:
                self.value = value

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.gate_type == "AND":
            self.draw_and_gate(painter)
        elif self.gate_type == "OR":
            self.draw_or_gate(painter)
        elif self.gate_type == "NOT":
            self.draw_not_gate(painter)
        elif self.gate_type == "NAND":
            self.draw_nand_gate(painter)
        elif self.gate_type == "NOR":
            self.draw_nor_gate(painter)
        elif self.gate_type == "XOR":
            self.draw_xor_gate(painter)
        elif self.gate_type == "XNOR":
            self.draw_xnor_gate(painter)

    def draw_and_gate(self, painter):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, 80, 40)
        painter.drawArc(0, 0, 80, 40, 90 * 16, 180 * 16)

    def draw_or_gate(self, painter):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(0, 0)
        path.cubicTo(40, 20, 40, 20, 0, 40)
        path.moveTo(80, 0)
        path.cubicTo(40, 20, 40, 20, 80, 40)
        painter.drawPath(path)

    def draw_not_gate(self, painter):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon([QPointF(0, 0), QPointF(80, 20), QPointF(0, 40)])
        painter.drawEllipse(QPointF(85, 20), 5, 5)

    def draw_nand_gate(self, painter):
        self.draw_and_gate(painter)
        painter.drawEllipse(QPointF(85, 20), 5, 5)

    def draw_nor_gate(self, painter):
        self.draw_or_gate(painter)
        painter.drawEllipse(QPointF(85, 20), 5, 5)

    def draw_xor_gate(self, painter):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(5, 0)
        path.cubicTo(45, 20, 45, 20, 5, 40)
        path.moveTo(0, 0)
        path.cubicTo(40, 20, 40, 20, 0, 40)
        path.moveTo(80, 0)
        path.cubicTo(40, 20, 40, 20, 80, 40)
        painter.drawPath(path)

    def draw_xnor_gate(self, painter):
        self.draw_xor_gate(painter)
        painter.drawEllipse(QPointF(85, 20), 5, 5)


class IOElement(QGraphicsEllipseItem):
    def __init__(self, io_type, label):
        super().__init__(0, 0, 50, 50)
        self.io_type = io_type
        self.label = label
        self.setBrush(QBrush(Qt.green if io_type == 'Giriş' else Qt.red))
        self.setPen(QPen(Qt.black, 2))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.text = QGraphicsSimpleTextItem(label, self)
        self.text.setPos(15, 15)
        self.value = 0 if io_type == 'Giriş' else None

    def contextMenuEvent(self, event):
        menu = QMenu()
        label_action = menu.addAction("Etiketi Ayarla")
        color_action = menu.addAction("Rengi Ayarla")

        if self.io_type == 'Giriş':
            value_action = menu.addAction("Başlangıç Değerini Ayarla")

        action = menu.exec_(event.screenPos())

        if action == label_action:
            text, ok = QInputDialog.getText(None, "Etiketi Ayarla", "Yeni etiketi girin:")
            if ok:
                self.text.setText(text)
                self.label = text
        elif action == color_action:
            color = QColorDialog.getColor()
            if color.isValid():
                self.setBrush(QBrush(color))
        elif action == value_action and self.io_type == 'Giriş':
            value, ok = QInputDialog.getInt(None, "Başlangıç Değerini Ayarla", "Başlangıç değeri (0 veya 1):", 0, 0, 1)
            if ok:
                self.value = value


class LED(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__(0, 0, 20, 20)
        self.setBrush(QBrush(Qt.yellow))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.text = QGraphicsSimpleTextItem("LED", self )
        self.text.setPos(25, 25)

    def contextMenuEvent(self, event):
        menu = QMenu()
        color_action = menu.addAction("Rengi Ayarla")

        action = menu.exec_(event.screenPos())

        if action == color_action:
            color = QColorDialog.getColor()
            if color.isValid():
                self.setBrush(QBrush(color))

class Connection(QGraphicsLineItem):
    def __init__(self, start_item, end_item, label):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.label = label
        self.setPen(QPen(Qt.black, 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.update_position()
        self.text = QGraphicsSimpleTextItem(label, self)
        self.text.setPos((self.start_item.sceneBoundingRect().center() + self.end_item.sceneBoundingRect().center()) / 2)

    def update_position(self):
        line = QLineF(self.start_item.sceneBoundingRect().center(), self.end_item.sceneBoundingRect().center())
        self.setLine(line)

    def contextMenuEvent(self, event):
        menu = QMenu()
        label_action = menu.addAction("Etiketi Ayarla")
        color_action = menu.addAction("Rengi Ayarla")

        action = menu.exec_(event.screenPos())

        if action == label_action:
            text, ok = QInputDialog.getText(None, "Etiketi Ayarla", "Yeni etiketi girin:")
            if ok:
                self.text.setText(text)
                self.label = text
        elif action == color_action:
            color = QColorDialog.getColor()
            if color.isValid():
                self.setPen(QPen(color, 2))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mantık Devresi Tasarlayıcı")
        self.setGeometry(100, 100, 1200, 800)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)
        self.createActions()
        self.createMenus()
        self.createToolbar()
        self.createSidebar()

        self.gates = []
        self.connections = []
        self.io_elements = []
        self.leds = []
        self.current_connection = False
        self.connection_start = None
        self.line_item = None

    def createActions(self):
        self.add_and_gate_action = QAction("AND Kapısı Ekle", self)
        self.add_and_gate_action.triggered.connect(lambda: self.add_gate("AND"))

        self.add_or_gate_action = QAction("OR Kapısı Ekle", self)
        self.add_or_gate_action.triggered.connect(lambda: self.add_gate("OR"))

        self.add_not_gate_action = QAction("NOT Kapısı Ekle", self)
        self.add_not_gate_action.triggered.connect(lambda: self.add_gate("NOT"))

        self.add_nand_gate_action = QAction("NAND Kapısı Ekle", self)
        self.add_nand_gate_action.triggered.connect(lambda: self.add_gate("NAND"))

        self.add_nor_gate_action = QAction("NOR Kapısı Ekle", self)
        self.add_nor_gate_action.triggered.connect(lambda: self.add_gate("NOR"))

        self.add_xor_gate_action = QAction("XOR Kapısı Ekle", self)
        self.add_xor_gate_action.triggered.connect(lambda: self.add_gate("XOR"))

        self.add_xnor_gate_action = QAction("XNOR Kapısı Ekle", self)
        self.add_xnor_gate_action.triggered.connect(lambda: self.add_gate("XNOR"))

        self.add_input_action = QAction("Giriş Ekle", self)
        self.add_input_action.triggered.connect(lambda: self.add_io_element("Giriş"))

        self.add_output_action = QAction("Çıkış Ekle", self)
        self.add_output_action.triggered.connect(lambda: self.add_io_element("Çıkış"))

        self.add_led_action = QAction("LED Ekle", self)
        self.add_led_action.triggered.connect(self.add_led)

        self.add_connection_action = QAction("Bağlantı Ekle", self)
        self.add_connection_action.triggered.connect(self.activate_connection_mode)

        # Yeni butonlar eklendi
        self.start_simulation_action = QAction("Başlat", self)
        self.stop_simulation_action = QAction("Durdur", self)
        self.reset_simulation_action = QAction("Sıfırla", self)

    def createMenus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Dosya")
        edit_menu = menubar.addMenu("Düzenle")
        view_menu = menubar.addMenu("Görünüm")
        simulation_menu = menubar.addMenu("Simülasyon")

        simulation_menu.addAction(self.add_led_action)
        simulation_menu.addAction(self.add_connection_action)

        # Yeni butonlar eklendi
        simulation_menu.addAction(self.start_simulation_action)
        simulation_menu.addAction(self.stop_simulation_action)
        simulation_menu.addAction(self.reset_simulation_action)

    def createToolbar(self):
        toolbar = self.addToolBar("Araçlar")
        toolbar.addAction(self.add_and_gate_action)
        toolbar.addAction(self.add_or_gate_action)
        toolbar.addAction(self.add_not_gate_action)
        toolbar.addAction(self.add_nand_gate_action)
        toolbar.addAction(self.add_nor_gate_action)
        toolbar.addAction(self.add_xor_gate_action)
        toolbar.addAction(self.add_xnor_gate_action)
        toolbar.addAction(self.add_input_action)
        toolbar.addAction(self.add_output_action)

    def createSidebar(self):
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        self.auto_draw_checkbox = QCheckBox("Oto Çiz")

        sidebar_layout.addWidget(self.auto_draw_checkbox)

        sidebar.setLayout(sidebar_layout)

        dock_widget = QDockWidget("Kontroller", self)
        dock_widget.setWidget(sidebar)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

    def add_gate(self, gate_type):
        gate = LogicGate(gate_type, gate_type)
        self.scene.addItem(gate)
        self.gates.append(gate)

    def add_io_element(self, io_type):
        io_element = IOElement(io_type, io_type)
        self.scene.addItem(io_element)
        self.io_elements.append(io_element)

    def add_led(self):
        led = LED()
        self.scene.addItem(led)
        self.leds.append(led)

    def activate_connection_mode(self):
        self.current_connection = True
        self.connection_start = None
        self.line_item = None

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, (LogicGate, IOElement, LED)):
            if event.button() == Qt.LeftButton:
                if self.current_connection:
                    if self.connection_start:
                        end_item = item
                        self.current_connection = False
                        self.line_item.setLine(QLineF(self.line_item.line().p1(), end_item.sceneBoundingRect().center()))
                        self.scene.removeItem(self.line_item)
                        connection = Connection(self.connection_start, end_item, f"Bağlantı {len(self.connections) + 1}")
                        self.scene.addItem(connection)
                        self.connections.append(connection)
                    else:
                        self.connection_start = item
                        self.line_item = QGraphicsLineItem(QLineF(item.sceneBoundingRect().center(), event.pos()))
                        self.scene.addItem(self.line_item)
            elif event.button() == Qt.RightButton:
                item.contextMenuEvent(event)

    def mouseMoveEvent(self, event):
        if self.current_connection and self.line_item:
            self.line_item.setLine(QLineF(self.line_item.line().p1(), self.mapToScene(event.pos())))

    def mouseReleaseEvent(self, event):
        if self.current_connection and isinstance(self.itemAt(event.pos()), QGraphicsScene):
            self.scene.removeItem(self.line_item)
            self.current_connection = False
            self.connection_start = None
            self.line_item = None

    def itemAt(self, pos):
        return self.scene.itemAt(self.view.mapToScene(pos), QTransform())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
