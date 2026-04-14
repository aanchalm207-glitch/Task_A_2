#include <iostream>
#include <cmath>
#include <unistd.h>

void update_joint_position(float target, float max_vel, float max_accel) {
    static float current_pos = 0.0f;      // current position (starts at 0)
    static float current_vel = 0.0f;      // current velocity
    static int phase = 0;                 // 0=ACCEL, 1=CRUISE, 2=DECEL, 3=DONE
    static float peak_vel = 0.0f;         // actual max velocity (max_vel or lower)
    static float accel_distance = 0.0f;   // distance spent accelerating
    static float decel_start_pos = 0.0f;  // position where deceleration begins
    static float prev_target = 0.0f;      // to detect when target changes

    if (target != prev_target) {      // if the target changes
        current_pos = 0.0f;
        current_vel = 0.0f;
        phase = 0;
        prev_target = target;

        float dist_reqd = (max_vel * max_vel) / (2.0f * max_accel);   //distance required to reach max velocity

        if (2.0f * dist_reqd < target) {     //trapezoid condition
            peak_vel = max_vel;
            accel_distance = dist_reqd;
            decel_start_pos = target - dist_reqd;
        }
        else {
            peak_vel = std::sqrt(max_accel * target);     //triangle condition
            accel_distance = target / 2.0f;
            decel_start_pos = target / 2.0f;
        }
    }

    if (phase == 3) {         // completed
        std::cout << current_pos << std::endl;
        return;
    }

    const float dt = 0.001f;   //time 1ms

    if (phase == 0) {     //ACCEL
        current_vel += max_accel * dt;
        if (current_vel >= peak_vel) {
            current_vel = peak_vel;
            phase = 1;
        }
    }

    else if (phase == 1) {     //CRUISE
        current_vel = peak_vel;
    }

    else if (phase == 2) {     //DECEL
        current_vel -= max_accel * dt;
        if (current_vel <= 0.0f) {
            current_vel = 0.0f;
        }
    }

    current_pos += current_vel * dt;   //updating current position

    if (phase == 0) {    //if the position crosses target while accelerating
        if (current_pos >= decel_start_pos) {
            phase = 2;
        }
    }
    else if (phase == 1) {     //if the position crosses target while cruising
        if (current_pos >= decel_start_pos) {
            phase = 2;
        }
    }
    else if (phase == 2) {     //if velocity is zero but position is ahead of target
        if (current_vel == 0.0f && current_pos >= target) {
            current_pos = target;
            phase = 3;
        }
    }

    if (current_pos > target && phase != 3) {    //if position is ahead of target and phase three is reached
        current_pos = target;
        current_vel = 0.0f;
        phase = 3;
    }

    std::cout << current_pos << std::endl;
}


int main() {     //calling the function to check output values
    float target = 5.0f;
    float max_vel = 2.0f;
    float max_accel = 4.0f;
    const int total_calls = 2000;

    for (int i = 0; i < total_calls; ++i) {
        update_joint_position(target, max_vel, max_accel);

    }

    return 0;
}
