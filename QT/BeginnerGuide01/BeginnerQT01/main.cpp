#include <QApplication>
#include <QPushButton>

#include "window.h"

int main(int argc, char **argv)
{
    QApplication app (argc, argv);

//    QPushButton button ("Hello world !");
//    button.setText("My text");
//    button.setToolTip("A tooltip");

//    QFont font ("Courier");
//    font.setPixelSize(23);
//    button.setFont(font);

//    button.setIcon(QIcon::fromTheme("face-smile"));

//    button.show();

//    QPushButton button1 ("test");
//    QPushButton button2 ("other", &button1);

//    button1.show();

    Window window;
    window.show();

    return app.exec();
}
