#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "include/motors.h"

// UART defines
#define UART_ID uart0
#define BAUD_RATE 9600

// Use pins 28 and 29 for UART0
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define UART_TX_PIN 28
#define UART_RX_PIN 29

char ch;
bool forward;
bool left;

void uart_config(){
    // Set up our UART
    uart_init(UART_ID, BAUD_RATE);
    // Set the TX and RX pins by using the function select on the GPIO
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
}

void motor_config(){
    //Don't divide clock
    motors_init(1);
}

int main()
{
    stdio_init_all();
    
    motor_config();
    uart_config();

    forward = true;
    left = true;
    uint16_t duty_cycle = (uint16_t)(.1 * MAX_MOTOR_POWER);


    while (true) {
        sleep_ms(1000);
        if(uart_is_readable(UART_ID)){
            ch = uart_getc(UART_ID);

            if (ch == 'u'){
                uart_putc(UART_ID, ch);
                motors_set_power(duty_cycle, forward, left);
                motors_set_power(duty_cycle, forward, !left);
            } else if(ch == 'l'){
                uart_putc(UART_ID, ch);
                motors_set_power(duty_cycle, !forward, left);
                motors_set_power(duty_cycle, forward, !left);

            } else if(ch == 'r'){
                uart_putc(UART_ID, ch);
                motors_set_power(duty_cycle, forward, left);
                motors_set_power(duty_cycle, !forward, !left);

            } else if(ch == 'b'){
                uart_putc(UART_ID, ch);
                motors_set_power(duty_cycle, !forward, left);
                motors_set_power(duty_cycle, !forward, !left);

            }
        }
    }
}
