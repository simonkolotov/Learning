#include <QApplication>
#include "window.h"

Window::Window(QWidget *parent) :
    QWidget(parent)
{
    int elementHeight = 10;
    QSize windowSize = QSize(300, 8*elementHeight);

    QRect progressBarGeometry = QRect(elementHeight, elementHeight,
                                           windowSize.width()-elementHeight*2, elementHeight);

    QRect sliderGeometry = QRect(elementHeight*3 , elementHeight*3 ,
                                      windowSize.width()-elementHeight *6, elementHeight);

    QRect quitButtonGeometry = QRect(windowSize.width()/2-elementHeight*2, elementHeight*5,
                                          elementHeight*4, elementHeight*2);

    m_sliderRange[0] = 0; m_sliderRange[1] = 200;

    // Set size of the window
    setFixedSize(windowSize);

    //Create a slider
    m_slider = new QSlider(this);
    m_slider->setOrientation(Qt::Horizontal);
    m_slider->setRange(m_sliderRange[0], m_sliderRange[1]);
    m_slider->setValue(50);
    m_slider->setGeometry(sliderGeometry);

    //Create a progress bar reflecting the slider
    m_progressBar = new QProgressBar(this);
    m_progressBar->setRange(0,100);
    m_progressBar->setGeometry(progressBarGeometry);
    connect(m_slider, SIGNAL(valueChanged(int)), this, SLOT(slotNormalizeValue(int)));
    connect(this, SIGNAL(normalizedValue(int)), m_progressBar, SLOT(setValue(int)));

    // Create and position the QUIT button
    m_button = new QPushButton("Quit", this);
    m_button->setGeometry(quitButtonGeometry);
    connect(m_button, SIGNAL(clicked()), QApplication::instance(), SLOT(quit()));

}

void Window::slotNormalizeValue(int value)
{
    //Normalize the signal received from the slider by the slider span
    emit this->normalizedValue(100*((float)(value-m_sliderRange[0])/(m_sliderRange[1]-m_sliderRange[0])));
}


