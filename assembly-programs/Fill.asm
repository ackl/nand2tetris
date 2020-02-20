// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.



// Listens to keyboard for keypresses
(LISTEN)
	@16384 // Store beginning of screen address in memory
	D=A
	@scrn
	M=D

	@256 // Store number of rows in register R1
	D=A
	@R1
	M=D

	// Check for keypress
	@KBD // 0x6000
	D=M

	@CLEAR
	D;JEQ
	@FILL
	D;JGT




// Fills screen address space with 16bit words of all 0 or 1
// Draws recursively from the top row
(DRAW)
	@32
	D=A
	@R0
	M=D

	@R1
	M=M-1
	D=M
	@DRAWROW
	D;JGT
	@LISTEN
	D;JEQ



// Subroutine for drawing a row
(DRAWROW)
	@R0
	M=M-1

	@R2
	D=M
	@scrn
	A=M
	M=D
	@scrn
	M=M+1

	@R0
	D=M
	@DRAWROW
	D;JGT
	@DRAW
	D;JEQ



(CLEAR)
	@R2
	M=0
	@DRAW
	0;JMP
(FILL)
	@R2
	M=-1
	@DRAW
	0;JMP