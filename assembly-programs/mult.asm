// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)


// initialise sum of product as 0
@R2 // put address of R2 into A
M=0	// set R2 to 0

// check to see if R0 is 0, if so just jump to end
@R0
D=M
@END
D;JEQ

// check to see if R1 is 0, if so just jump to end
@R1
D=M
@END
D;JEQ

(LOOP)
@R0
D=M // put value of R0 into D register

@R2 // load current sum
M=D+M // add current sum with R0

@R1 // decrement amount of times we need to add R0 to itself by one
M=M-1
D=M

@LOOP
D;JGT

(END)
@END
0;JMP