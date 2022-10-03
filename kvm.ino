/** IP-KVM Support:
 *  HID KeyBoard Controlling
 *  ATX Power Supply Controlling
 */
#include <Keyboard.h>
#define PWR 6           // PWR button signal
#define RST 9           // RST button signal

#define PSC_FIELD 0xfd  // Command used for power supply controlling
#define KEY_RLS   0x00  // Key release command
#define KEY_PRS   0x01  // Key press command
#define PWR_S     0xfd  // Short press power button command
#define RST_S     0xfe  // Short press reset button command
#define PWR_L     0xff  // Long press power button command

bool bPress = true;

void setup()
{
    digitalWrite(PWR, LOW);
    digitalWrite(RST, LOW);
    pinMode(PWR, OUTPUT);
    pinMode(RST, OUTPUT);
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
            else                    // Emulate keyboard press/release
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
}
