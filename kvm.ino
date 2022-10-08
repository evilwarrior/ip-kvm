/** IP-KVM Support:
 *  HID KeyBoard Controlling
 *  ATX Power Supply Controlling
 */
#include <Keyboard.h>
#define PWR 6           // PWR button emulator pin
#define RST 9           // RST button emulator pin
#define ORI_PWR   2     // Original power button pin
#define ORI_RST   21    // Original reset button pin

#define PSC_FIELD 0xfd  // Command used for power supply controlling
#define KEY_RLS   0x00  // Key release command
#define KEY_PRS   0x01  // Key press command
#define PWR_S     0xfd  // Short press power button command
#define RST_S     0xfe  // Short press reset button command
#define PWR_L     0xff  // Long press power button command

bool bPress = true;     // Is KeyBoard pressed?

void setup()
{
    // I/O Setup
    digitalWrite(PWR, LOW);
    digitalWrite(RST, LOW);
    pinMode(PWR, OUTPUT);
    pinMode(RST, OUTPUT);
    pinMode(ORI_PWR, INPUT);
    pinMode(ORI_RST, INPUT);
    digitalWrite(ORI_PWR, HIGH);
    digitalWrite(ORI_RST, HIGH);
    Serial1.begin(9600);  // Init hardware serial port
    Keyboard.begin();     // Init keyboard emulation
}

void loop()
{
    if (Serial1.available())    // Get command from serial
    {
        unsigned char cKey = Serial1.read();
        // HID KeyBoard Control
        if (cKey < PSC_FIELD)
        {
            if (cKey == KEY_RLS)       // Release some key
            {
                bPress = false;
            }
            else if (cKey == KEY_PRS)  // Press some key
            {
                bPress = true;
            }
            else                       // Emulate keyboard press/release
            {
                if (bPress)
                {
                    Keyboard.press(cKey);
                }
                else
                {
                    Keyboard.release(cKey);
                }
            }
        }
        // ATX Power Supply Control
        else
        {
            if (cKey == PWR_S)       // Emulate short press power button
            {
                digitalWrite(PWR, HIGH);
                delay(400);
                digitalWrite(PWR, LOW);
            }
            else if (cKey == RST_S)  // Emulate press reset button
            {
                digitalWrite(RST, HIGH);
                delay(400);
                digitalWrite(RST, LOW);
            }
            else if (cKey == PWR_L)  // Emulate press reset button
            {
                digitalWrite(PWR, HIGH);
                delay(5000);
                digitalWrite(PWR, LOW);
            }
        }
    }

    // Transform original power button input into power button emulator output
    int nSt = digitalRead(PWR);
    if (digitalRead(ORI_PWR) == nSt)
    {
        digitalWrite(PWR, nSt^0x01);
    }

    // Transform original reset button input into reset button emulator output
    nSt = digitalRead(RST);
    if (digitalRead(ORI_RST) == nSt)
    {
        digitalWrite(RST, nSt^0x01);
    }
}
