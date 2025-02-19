#ifndef REPORT_TIMES_H
#define REPORT_TIMES_H

#include <chrono>

using namespace std::chrono;

auto report_times(const steady_clock::duration& file_parse_time,
                  const steady_clock::duration& part1_time,
                  const steady_clock::duration& part2_time) -> void;

#endif  // REPORT_TIMES_H
