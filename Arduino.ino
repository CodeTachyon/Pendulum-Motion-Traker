#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
unsigned long previousTime = 0;
float ref_angle;  
float cal_angle;
void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    while (1);
  }

  Serial.println("MPU6050 ready");
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // Calculate angle from acceleration (assuming pendulum swings in X-Z plane)
  ref_angle = atan2(ax, az) * 180.0 / PI;
    delay(3000);
}

void loop() {

  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // Calculate angle from acceleration (assuming pendulum swings in X-Z plane)
  float angle = atan2(ax, az) * 180.0 / PI;
  cal_angle = angle - ref_angle;

  if (cal_angle > 180) cal_angle -= 360;
  else if (cal_angle < -180) cal_angle += 360;

  unsigned long currentTime = millis();
  float elapsedTime = (currentTime - previousTime) / 1000.0;
  previousTime = currentTime;

  Serial.print(cal_angle);
  Serial.print(",");
  Serial.println(currentTime / 1000.0);  // Time in seconds

  delay(20); // 50 Hz sampling
}
