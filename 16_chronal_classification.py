"""Solution to Advent of Code 2018 Day 16.

--- Day 16: Chronal Classification ---
As you see the Elves defend their hot chocolate successfully, you go back to
falling through time. This is going to become a problem.

If you're ever going to return to your own time, you need to understand how this
device on your wrist works. You have a little while before you reach your next
destination, and with a bit of trial and error, you manage to pull up a
programming manual on the device's tiny screen.

According to the manual, the device has four registers (numbered 0 through 3)
that can be manipulated by instructions containing one of 16 opcodes. The
registers start with the value 0.

Every instruction consists of four values: an opcode, two inputs (named A and
B), and an output (named C), in that order. The opcode specifies the behavior of
the instruction and how the inputs are interpreted. The output, C, is always
treated as a register.

In the opcode descriptions below, if something says "value A", it means to take
the number given as A literally. (This is also called an "immediate" value.) If
something says "register A", it means to use the number given as A to read from
(or write to) the register with that number. So, if the opcode addi adds
register A and value B, storing the result in register C, and the instruction
addi 0 7 3 is encountered, it would add 7 to the value contained by register 0
and store the sum in register 3, never modifying registers 0, 1, or 2 in the
process.

Many opcodes are similar except for how they interpret their arguments. The
opcodes fall into seven general categories:

Addition:

addr (add register) stores into register C the result of adding register A and
register B.
addi (add immediate) stores into register C the result of adding register A and
value B.
Multiplication:

mulr (multiply register) stores into register C the result of multiplying
register A and register B.
muli (multiply immediate) stores into register C the result of multiplying
register A and value B.
Bitwise AND:

banr (bitwise AND register) stores into register C the result of the bitwise AND
of register A and register B.
bani (bitwise AND immediate) stores into register C the result of the bitwise
AND of register A and value B.
Bitwise OR:

borr (bitwise OR register) stores into register C the result of the bitwise OR
of register A and register B.
bori (bitwise OR immediate) stores into register C the result of the bitwise OR
of register A and value B.
Assignment:

setr (set register) copies the contents of register A into register C. (Input B
is ignored.)
seti (set immediate) stores value A into register C. (Input B is ignored.)
Greater-than testing:

gtir (greater-than immediate/register) sets register C to 1 if value A is
greater than register B. Otherwise, register C is set to 0.
gtri (greater-than register/immediate) sets register C to 1 if register A is
greater than value B. Otherwise, register C is set to 0.
gtrr (greater-than register/register) sets register C to 1 if register A is
greater than register B. Otherwise, register C is set to 0.
Equality testing:

eqir (equal immediate/register) sets register C to 1 if value A is equal to
register B. Otherwise, register C is set to 0.
eqri (equal register/immediate) sets register C to 1 if register A is equal to
value B. Otherwise, register C is set to 0.
eqrr (equal register/register) sets register C to 1 if register A is equal to
register B. Otherwise, register C is set to 0.
Unfortunately, while the manual gives the name of each opcode, it doesn't seem
to indicate the number. However, you can monitor the CPU to see the contents of
the registers before and after instructions are executed to try to work them
out. Each opcode has a number from 0 through 15, but the manual doesn't say
which is which. For example, suppose you capture the following sample:

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
This sample shows the effect of the instruction 9 2 1 2 on the registers. Before
the instruction is executed, register 0 has value 3, register 1 has value 2, and
registers 2 and 3 have value 1. After the instruction is executed, register 2's
value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1,
and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only three of
them behave in a way that would cause the result shown in the sample:

Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1
(which has a value of 2) produces 2, which matches the value stored in the
output register, register 2.
Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1
produces 2, which matches the value stored in the output register, register 2.
Opcode 9 could be seti: value 2 matches the value stored in the output register,
register 2; the number given for B is irrelevant.
None of the other opcodes produce the result captured in the sample. Because of
this, the sample above behaves like three opcodes.

You collect many of these samples (the first section of your puzzle input). The
manual also includes a small test program (the second section of your puzzle
input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input behave like
three or more opcodes?

--- Part Two ---
Using the samples you collected, work out the number of each opcode and execute
the test program (the second section of your puzzle input).

What value is contained in register 0 after executing the test program?
"""

import copy
import functools


def _executer(registers, instruction, op):
  _, a, b, c = instruction
  registers[c] = op(registers[a], registers[b])


def _executei(registers, instruction, op):
  _, a, b, c = instruction
  registers[c] = op(registers[a], b)


def _setr(registers, instruction):
  _, a, _, c = instruction
  registers[c] = registers[a]


def _seti(registers, instruction):
  _, a, _, c = instruction
  registers[c] = a


def _testir(registers, instruction, op):
  _, a, b, c = instruction
  registers[c] = op(a, registers[b])


def _testri(registers, instruction, op):
  _, a, b, c = instruction
  registers[c] = op(registers[a], b)


def _testrr(registers, instruction, op):
  _, a, b, c = instruction
  registers[c] = op(registers[a], registers[b])


OPS = {
    'addr': functools.partial(_executer, op=lambda x, y: x + y),
    'addi': functools.partial(_executei, op=lambda x, y: x + y),
    'mulr': functools.partial(_executer, op=lambda x, y: x * y),
    'muli': functools.partial(_executei, op=lambda x, y: x * y),
    'banr': functools.partial(_executer, op=lambda x, y: x & y),
    'bani': functools.partial(_executei, op=lambda x, y: x & y),
    'borr': functools.partial(_executer, op=lambda x, y: x | y),
    'bori': functools.partial(_executei, op=lambda x, y: x | y),
    'setr': _setr,
    'seti': _seti,
    'gtir': functools.partial(_testir, op=lambda x, y: int(x > y)),
    'gtri': functools.partial(_testri, op=lambda x, y: int(x > y)),
    'gtrr': functools.partial(_testrr, op=lambda x, y: int(x > y)),
    'eqir': functools.partial(_testir, op=lambda x, y: int(x == y)),
    'eqri': functools.partial(_testri, op=lambda x, y: int(x == y)),
    'eqrr': functools.partial(_testrr, op=lambda x, y: int(x == y)),
}


def _to_list(string):
  string = string.replace(',', '')
  return [int(s) for s in string.split()]


def find_similar_ops(before, instruction, after, ops=None):
  ops = ops or OPS
  opnames = []
  for key, op in ops.items():
    registers = copy.deepcopy(before)
    op(registers, instruction)
    if registers == after:
      opnames.append(key)
  return opnames


if __name__ == '__main__':
  with open('input/16') as file_:
    lines = file_.read().splitlines()
  samples = []
  program = []
  i = 0
  while i < len(lines):
    if lines[i]:
      if lines[i].startswith('Before:'):
        before = _to_list(lines[i][9:-1])
        instruction = _to_list(lines[i + 1])
        after = _to_list(lines[i + 2][9:-1])
        samples.append((before, instruction, after))
        i += 2
      else:
        program.append(_to_list(lines[i]))
    i += 1

  # Part 1.
  result = 0
  for before, instruction, after in samples:
    opnames = find_similar_ops(before, instruction, after)
    if len(opnames) >= 3:
      result += 1
  print('Samples behaving like 3 or more:', result)

  # Part 2.
  result = 0
  code_to_name = {}
  while True:
    ops = {k: v for k, v in OPS.items() if k not in code_to_name.values()}
    if not ops:
      break
    for before, instruction, after in samples:
      opcode = instruction[0]  # Skip if we already know the op.
      if opcode in code_to_name:
        continue
      opnames = find_similar_ops(before, instruction, after, ops)
      if len(opnames) == 1:
        opname = opnames[0]
        code_to_name[opcode] = opname
        break
  registers = [0, 0, 0, 0]
  for instruction in program:
    opcode = instruction[0]
    opname = code_to_name[opcode]
    op = OPS[opname]
    op(registers, instruction)
  print('Output of register 0:', registers[0])

