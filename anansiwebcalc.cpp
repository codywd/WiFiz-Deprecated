#include "anansiwebcalc.h"
#include "ui_anansiwebcalc.h"

AnansiWebCalc::AnansiWebCalc(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::AnansiWebCalc)
{
    ui->setupUi(this);
    textl="";
        ui->lineEdit->setAlignment(Qt::AlignRight);
        ui->lineEdit->setMaxLength(12);
        ans=0;

        QObject::connect(ui->btnAdd,SIGNAL(clicked()),this,SLOT(addi()));
        QObject::connect(ui->btnMinus, SIGNAL(clicked()),this,SLOT(subs()));
        QObject::connect(ui->btnMult, SIGNAL(clicked()),this,SLOT(mult()));
        QObject::connect(ui->btnDiv, SIGNAL(clicked()),this, SLOT(divi()));
        QObject::connect(ui->equalsBtn, SIGNAL(clicked()),this,SLOT(em()));
        QObject::connect(ui->btn1,SIGNAL(clicked()),this,SLOT(mone()));
        QObject::connect(ui->btn2,SIGNAL(clicked()),this,SLOT(mtwo()));
        QObject::connect(ui->btn3,SIGNAL(clicked()),this,SLOT(mthree()));
        QObject::connect(ui->btn4,SIGNAL(clicked()),this,SLOT(mfour()));
        QObject::connect(ui->btn5,SIGNAL(clicked()),this,SLOT(mfive()));
        QObject::connect(ui->btn6,SIGNAL(clicked()),this,SLOT(msix()));
        QObject::connect(ui->btn7,SIGNAL(clicked()),this,SLOT(mseven()));
        QObject::connect(ui->btn8,SIGNAL(clicked()),this,SLOT(meight()));
        QObject::connect(ui->btn9,SIGNAL(clicked()),this,SLOT(mnine()));
        QObject::connect(ui->btn0,SIGNAL(clicked()),this,SLOT(mzero()));
        QObject::connect(ui->btnClearCur,SIGNAL(clicked()),this,SLOT(mreset()));
        QObject::connect(ui->btnClearAll,SIGNAL(clicked()),this,SLOT(mreset()));
        QObject::connect(ui->btnDecimal,SIGNAL(clicked()),this,SLOT(mdot()));
        QObject::connect(ui->actionClear_All,SIGNAL(triggered()),this,SLOT(mreset()));
        QObject::connect(ui->actionExit,SIGNAL(triggered()),this,SLOT(close()));
        QObject::connect(ui->btnPi,SIGNAL(clicked()),this,SLOT(mpi()));
        QObject::connect(ui->btnXSq,SIGNAL(clicked()),this,SLOT(mXSq()));
}

AnansiWebCalc::~AnansiWebCalc()
{
    delete ui;
}

void AnansiWebCalc::mreset()
{
    textl="";
    ui->lineEdit->clear();
}

void AnansiWebCalc::mXSq()
{
    if(ui->lineEdit->text() == "")
    {
        ui->lineEdit->setText("Please insert a number first.");
    }
    else
    {
        str=ui->lineEdit->text();
        num=str.toFloat();
        ans = num*num;
        strResult = strResult.number(ans);
        ui->lineEdit->setText(strResult);
        textl=strResult;
    }
}

void AnansiWebCalc::mpi()
{

}

void AnansiWebCalc::mdot()
{
        textl=ui->btnDecimal->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::mone()
{
        textl=ui->btn1->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::mtwo()
{
        textl=ui->btn2->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::mthree()
{
        textl=ui->btn3->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::mfour()
{
        textl=ui->btn4->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::mfive()
{
        textl=ui->btn5->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::msix()
{
        textl=ui->btn6->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::mseven()
{
        textl=ui->btn7->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::meight()
{
        textl=ui->btn8->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::mnine()
{
        textl=ui->btn9->text();
        ui->lineEdit->setText(textl);
}

void AnansiWebCalc::mzero()
{
        textl=ui->btn0->text();
        ui->lineEdit->setText(textl);

}

void AnansiWebCalc::addi()
{
    str=ui->lineEdit->text();
    num=str.toFloat();
    ch=ui->btnAdd->text();
    ui->lineEdit->clear();
    textl="";
}

void AnansiWebCalc::subs()
{
    str=ui->lineEdit->text();
    num=str.toFloat();
    ch=ui->btnMinus->text();
    ui->lineEdit->clear();
    textl="";
}

void AnansiWebCalc::mult()
{
    str=ui->lineEdit->text();
    num=str.toFloat();
    ch=ui->btnMult->text();
    ui->lineEdit->clear();
    textl="";
}

void AnansiWebCalc::divi()
{
    str=ui->lineEdit->text();
    num=str.toFloat();
    ch=ui->btnDiv->text();
    ui->lineEdit->clear();
    textl="";
}

void AnansiWebCalc::em()
{
    strl = ui->lineEdit->text();
    numl = strl.toFloat();
    if (ch=="+")
    {
        ans=num+numl;
    }
    else if(ch=="-")
    {
        ans=num-numl;
    }
    else if(ch=="*")
    {
        ans=num*numl;
    }
    else if(ch=="/")
    {
        ans=num/numl;
    }
    else
    {
        strResult = strResult.number(ans);
        ui->lineEdit->setText(strResult);
    }
    strResult = strResult.number(ans);
    ui->lineEdit->setText(strResult);
    ch="";
    textl=strResult;
}
