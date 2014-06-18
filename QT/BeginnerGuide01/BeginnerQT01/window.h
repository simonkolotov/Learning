#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>
#include <QPushButton>
#include <QProgressBar>
#include <QSlider>
#include <QRect>
#include <QSize>

class Window : public QWidget
{
    Q_OBJECT
public:
    explicit Window(QWidget *parent = 0);

signals:
    int normalizedValue(int);

private slots:
    void slotNormalizeValue(int value);

private:
    QPushButton *m_button;
    QProgressBar *m_progressBar;
    QSlider *m_slider;

    int m_sliderRange[2];

};

#endif // WINDOW_H
