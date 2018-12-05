"""Solution for Advent of Code 2018 Day 1.

NOTE(eugenhotaj): part 1 requires no code. Simply copy and paste the input into
a python interpreter with 0 prepended, e.g.: 0 + <input> = answer.

--- Day 1: Chronal Calibration ---
"We've detected some temporal anomalies," one of Santa's Elves at the Temporal
Anomaly Research and Detection Instrument Station tells you. She sounded pretty
worried when she called you down here. "At 500-year intervals into the past,
someone has been changing Santa's history!"

"The good news is that the changes won't propagate to our time stream for
another 25 days, and we have a device" - she attaches something to your wrist -
"that will let you fix the changes with no such propagation delay. It's
configured to send you 500 years further into the past every few days; that was
the best we could do on such short notice."

"The bad news is that we are detecting roughly fifty anomalies throughout time;
the device will indicate fixed anomalies with stars. The other bad news is that
we only have one device and you're the best person for the job! Good lu--" She
taps a button on the device and you suddenly feel like you're falling. To save
Christmas, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day
in the advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants one star. Good luck!

After feeling like you've been falling for a few minutes, you look at the
device's tiny screen. "Error: Device must be calibrated before first use.
Frequency drift detected. Cannot maintain destination lock." Below the message,
the device shows a sequence of changes in frequency (your puzzle input). A value
like +6 means the current frequency increases by 6; a value like -3 means the
current frequency decreases by 3.

For example, if the device displays frequency changes of +1, -2, +3, +1, then
starting from a frequency of zero, the following changes would occur:

Current frequency  0, change of +1; resulting frequency  1.
Current frequency  1, change of -2; resulting frequency -1.
Current frequency -1, change of +3; resulting frequency  2.
Current frequency  2, change of +1; resulting frequency  3.
In this example, the resulting frequency is 3.

Here are other example situations:

+1, +1, +1 results in  3
+1, +1, -2 results in  0
-1, -2, -3 results in -6
Starting with a frequency of zero, what is the resulting frequency after all of
the changes in frequency have been applied?

--- Part Two ---
You notice that the device repeats the same frequency change list over and over.
To calibrate the device, you need to find the first frequency it reaches twice.

For example, using the same list of changes above, the device would loop as
follows:

Current frequency  0, change of +1; resulting frequency  1.
Current frequency  1, change of -2; resulting frequency -1.
Current frequency -1, change of +3; resulting frequency  2.
Current frequency  2, change of +1; resulting frequency  3.
(At this point, the device continues from the start of the list.)
Current frequency  3, change of +1; resulting frequency  4.
Current frequency  4, change of -2; resulting frequency  2, which has already
been seen.
In this example, the first frequency reached twice is 2. Note that your device
might need to repeat its list of frequency changes many times before a duplicate
frequency is found, and that duplicates might be found while in the middle of
processing the list.

Here are other examples:

+1, -1 first reaches 0 twice.
+3, +3, +4, -2, -4 first reaches 10 twice.
-6, +3, +8, +5, -6 first reaches 5 twice.
+7, +7, -2, -7, -4 first reaches 14 twice.
What is the first frequency your device reaches twice?
"""

data = [
    +7, -5, -9, -1, -3, +7, -8, -17, -4, -18, -15, +18, -11, -3, -15, +6, +17,
    -3, +19, +6, +4, -15, +18, -14, +8, -11, -7, -15, +19, -1, +10, +18, -1, +5,
    -12, +11, -5, +17, +9, -12, +7, +19, -9, +17, +12, -15, -12, +11, +14, -16,
    -13, +7, +5, -6, +20, -1, +8, -13, -6, -9, +4, +23, -5, -5, -19, +20, -6,
    +21, -4, +12, +10, -1, +16, +15, -12, -17, -3, +9, -19, -3, +7, -5, -7, -8,
    +2, +7, +16, -2, +13, +13, +20, -15, -10, -5, -1, +7, -15, +18, +3, -1, +16,
    -13, -1, -10, +15, -17, -18, -11, +1, +2, +7, +12, -14, +22, +14, +5, -13,
    -16, +25, +20, +2, +10, +16, -19, -1, -7, +3, +3, +10, +4, +16, +12, +8, +7,
    -12, -1, -7, +19, -4, +11, +18, -15, +12, +11, -10, -7, +12, -16, +2, -5,
    -5, +14, +9, +14, +19, +11, +6, +13, +14, +14, -6, -9, -9, -11, -5, -5, +15,
    -7, +1, -17, +7, -15, -7, +12, -6, -13, -19, +10, +5, -1, +6, +20, -12, -7,
    +18, -17, -15, -11, +16, +12, +13, -21, +9, +9, +11, -2, -13, -1, -6, +4,
    -16, +2, -5, +23, -13, -12, -19, +2, +2, -12, -6, +1, -21, -16, -18, +5,
    +18, +4, -11, +17, +3, +6, -1, -4, -18, +2, -4, -3, -15, -6, -1, -13, +10,
    +15, +6, +20, +18, -9, +11, -3, -18, -16, -1, +20, -7, +19, -24, +20, +12,
    +22, -15, +24, -21, +3, +13, -15, +23, +37, +9, +18, +3, -11, +20, +4, +15,
    +14, -5, +7, -6, +9, -2, -9, +12, +11, -18, +8, -15, +16, -7, +11, +11, +1,
    -8, +6, -8, +18, -21, +9, -7, +12, +4, +13, +15, +5, -10, -4, +10, -3, +24,
    -14, +10, +7, -11, -20, +19, +6, +7, +12, +1, +1, -7, +1, +20, +25, -14,
    -20, -15, -19, -23, -14, +9, -30, -13, -13, -20, +11, +15, -3, -9, +13, -12,
    -10, -9, +2, +19, -8, +3, -6, +18, -5, +15, -16, -10, -15, -6, -5, -10, +18,
    -16, +25, -15, -18, +12, +19, -12, +4, +6, +9, -27, -60, -48, -4, +2, -17,
    -12, +11, -18, -9, +5, -6, -28, +3, -13, +35, +5, +25, -22, -35, -15, -27,
    -10, -9, -64, -9, +10, -3, -25, +9, -14, -83, +11, +61, -8, -8, +12, +50,
    -20, -165, +7, -65, -3, -5, +281, +56, +121, -55464, +8, -9, -15, -3, -16,
    +10, -11, +9, +5, +4, +7, -20, -15, -1, -10, -11, +12, -11, +16, +21, -3,
    +4, +1, -9, -2, -6, -7, +9, -11, -1, -4, +15, -4, -13, -1, -1, +10, -17,
    -15, -17, +11, +9, +3, -9, +13, +2, -3, -17, +19, -16, -4, +8, -3, +5, -12,
    +16, +8, -15, -19, -8, -3, -13, -5, -16, +3, +2, +10, -5, +2, +14, +10, +8,
    -11, +2, -6, +9, +8, +7, +6, -3, -6, -11, +12, -23, -11, +13, +22, +18, +21,
    +18, +19, +6, -3, +5, +17, +7, -4, +13, -5, +13, +18, +10, -7, +12, +11,
    -10, -7, +14, +6, -16, +20, +16, -1, +6, -14, +15, -2, -25, +13, +39, -11,
    -9, +34, -60, -14, -22, -27, -12, -10, +3, +20, +3, +8, +7, -10, -14, +12,
    +9, -6, +8, -19, -10, -16, -14, +16, -4, -20, +10, -17, -9, -15, +16, +11,
    -20, -11, -14, -28, -16, -2, +21, -18, +17, +5, -6, -18, -15, -14, +15, +11,
    -16, -5, +19, -12, -15, -1, +11, -16, +11, +15, -19, +3, -9, -2, -9, +1, -5,
    +7, +11, +24, +14, +4, +17, -46, -5, -17, -8, -10, -12, -5, +10, +3, +9,
    +14, +7, -6, -16, +17, -18, +14, -10, +18, -17, -11, -17, -12, -15, -2, -4,
    -9, -13, +10, +4, -3, -9, -5, +7, +11, -17, -21, +9, +17, +17, +13, +12, -3,
    -3, +18, -5, +12, +10, +3, +10, +24, +21, +13, +22, +19, +72, +7, +11, -15,
    -5, +6, +83, +8, -153, +24, +8, +39, +43, -265, -17, +18, -4, -12, +7, -4,
    -2, +18, +12, +11, -7, -9, -4, +10, +15, +25, -20, -16, -22, -21, -11, +2,
    +13, +20, +10, +12, -6, -23, +3, -17, -7, +15, -19, -10, -8, -2, -8, -2, -6,
    +5, +7, -5, -3, -3, -15, +4, +5, +15, -12, -16, -13, +15, -4, -9, +12, -8,
    +2, +19, -4, +1, -23, -9, -10, -2, +5, -10, +2, -3, -10, -15, +19, -7, -9,
    -17, +10, -18, +16, -14, +7, -10, +12, +3, -7, +12, +21, -5, -11, -7, +3,
    +11, -16, +15, +14, +17, +8, -2, -1, +19, +10, +11, +22, -1, +18, +12, -19,
    -5, +17, -4, -4, +19, -46, -22, -11, +19, -12, -19, -11, -17, -15, -42, -11,
    -4, +20, +6, -38, +8, -58, +5, -11, -60, -7, -61, -5, +36, -82, -3, -35,
    -11, +33, -51, -17, +9, -277, +251, -55001, +3, -11, +1, +13, +3, -15, +1,
    +2, +7, -16, +13, +9, +18, -1, -10, +5, +17, -9, +2, +10, +18, +19, +3, -9,
    -18, -4, +6, -13, +6, +19, +15, +14, -13, +17, +14, -3, -7, -16, -9, +16,
    -5, -12, +19, +16, -15, +12, -5, +7, -20, -6, -1, +6, -7, +17, +22, +7, -13,
    +8, +16, +14, -18, +12, -4, -1, +10, -15, +14, +11, +9, -14, -3, +10, -8,
    -8, -16, +18, -4, +17, -3, -22, -18, -20, +19, -6, +14, -1, +4, +15, -4,
    +24, -31, -10, +7, -24, -1, +8, +4, -21, +8, -4, -16, +2, +4, -18, +6, -5,
    -19, -6, -5, -13, +17, +15, -5, +4, +2, -19, +12, -16, -8, -11, +3, +14, -5,
    +8, +17, -5, -11, +23, +2, -18, -30, -11, +5, +15, -14, -17, +13, +19, +2,
    -15, -7, -18, -14, -3, -2, -6, -12, +1, +20, +5, +2, -3, -20, -3, +9, -15,
    -4, -6, +2, +3, +19, +17, -3, -18, -17, -20, +14, +2, -18, +13, +13, -21,
    -13, -4, -18, +11, +1, +3, +10, -15, -4, -7, -2, -16, -11, -10, -5, +6, +1,
    -12, -8, -5, -10, +1, +5, +15, -14, -5, -3, -14, +19, +111653
]

if __name__ == '__main__':
  # Part 2.
  seen = set()
  i = 0
  curr_frequency = 0
  seen.add(curr_frequency)
  while True:
    curr_frequency += data[i]
    if curr_frequency in seen:
      print('First double frequency: ', curr_frequency)
      break
    seen.add(curr_frequency)
    i = (i + 1) % len(data)
