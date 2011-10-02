#include <QtGui/QApplication>
#include "anansiwebcalc.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    AnansiWebCalc w;
    w.show();

    return a.exec();
}
