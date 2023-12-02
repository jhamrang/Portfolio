TITLE Project_6_931981933    (Project_6_931981933.asm)

; Author: John Hamrang
; Last Modified: 12/05/2021
; OSU email address: hamrangj@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number:	4             Due Date:		12/05/2021
; Description: Take 10 numbers and using string primitives and macros display the numbers, their sum, and their average



; (insert constant definitions here)

NUMUSERINPUT = 10							; amount of user input strings to enter

INCLUDE Irvine32.inc


.data
; Intro and prompts
intro_1		    BYTE	    "Name: John Hamrang			Project title: String Primitives and Macros: Project_6_931981933.asm.", 13, 10, 0
intro_2			BYTE		"Please enter 10 signed decimal integers. Numbers need to be able to fit in a 32 bit register. This program will display a list of the numbers, the sum, and the average of the numbers ", 13,10,0

prompt_1		BYTE		"Please enter a number: ",0
prompt_2		BYTE		"Previous number was invalid, please try again: " ,0
buffer			DWORD		13 DUP(0)

; Array data
int_array		SDWORD		10 DUP(?)		; Made to store numbers after they've been converted to ints from strings
int_temp		SDWORD		?
user_input		BYTE		13 DUP(0)		; stores initial user input string
temp_string		BYTE		13 DUP(0)		; ends up storing a reversed version of the user input string, probably could be made a local variable in writeval, but I wasnt sure how to initialize a string as a local
correct_string  BYTE		13 DUP(0)		; stores corrected user input string
average_string	BYTE		13 DUP(0)
sum_string		BYTE		13 DUP(0)

; Outro
outro_1			BYTE		"You've entered the following valid input: ", 0
comma			BYTE		", ", 0
outro_2			BYTE		"The sum ofthe numbers entered is: ", 0
outro_3			BYTE		"The average (truncated, not rounded) is: ",0
outro_4			BYTE		"Goodbye", 13, 10,0

; Goodbye statement
;goodbye	        BYTE	    "Goodbye. Have a good day!  ", 13, 10, 0 

; Macros

; Name: mDisplayString
;
; Displays string at passed location
;
; Preconditions: string location must be passed, as string must be passed by reference. So offset should be done before calling the macro
;
; Receives:
; stringLoc = location of string
;
; returns: None
; ---------------------------------------------
 mDisplayString MACRO	  stringLoc
   push		edx
   mov		edx,		 stringLoc
   call		writeString
   pop		edx

ENDM


; Name: mGetString
;
; Displays a prompt and then collects input and then returns a reference to it in edx
;
; Preconditions: promptLoc - is the location of the prompt. EDX can be overwritten, as it is used to return the location of the user inputted string. Buffer is the max size of the user input
;
; Receives:	promptLoc - Location of the prompt
;
; returns: user_input reference in EDX, num characters in  EAX
; ---------------------------------------------
 mGetString MACRO	  promptLoc, bufferOffset, bufferSize
   push		ecx
   ;push		edx
   mov		ecx,		bufferSize
   mov		edx,		bufferOffset
   mDisplayString		promptLoc
   call		ReadString
   ;pop		edx
   pop		ecx
  
ENDM


.code
main PROC
  mDisplayString	offset intro_1
  mDisplayString	offset intro_2
  ; Gather user input
  mov					ecx,			NUMUSERINPUT					; Figured we would be allowed to use a constant for the number of user inputs
  mov					edi,			offset int_array
  sub					edi,			4
  _readLoop:
	add					edi,			4								; incrementing by 4 so each loop is stepping through the array
	push				edi
	push				offset user_input
	push				offset int_temp
	push				offset buffer
	push				offset prompt_2	
	push				offset prompt_1	
	call				readVal
	dec					ecx
	cmp					ecx,				0
	JG					_readLoop
  
  ; Diplay valid user entries
  mDisplayString	offset outro_1

  mov				eax,				offset correct_string

  mov				ecx,				NUMUSERINPUT		
  mov				esi,				offset int_array
  sub				esi,				4
  mov				ebx,				0								; ebx is the sum of the values. Calculating sum in the writeLoop as well
  _writeLoop:
	
	push				ecx
	mov					eax,									0
	push				edi			
	; Clearing old user input out of correct string and temp string
	mov					ecx,					13
	mov					al,0
	mov					edi,					offset correct_string
	rep	stosb
	mov					ecx,					13
	mov					edi,					offset temp_string
	rep stosb		

	pop					edi
	pop					ecx
	mov					eax,					0

	add					esi,					4						; incrementing by 4 so each loop is stepping through the array
	mov					eax,					[esi]
	add					ebx,					eax						; calculating sum
  	mov					int_temp,				eax
	push				offset correct_string
  	push				offset temp_string
  	push				int_temp
  	call				writeVal
	dec					ecx
	cmp					ecx,					1
	JL					_no_comma
	mDisplayString		offset comma									; values get a comma placed between them
	_no_comma:
	cmp					ecx,				0	
	JG					_writeLoop
  
  ; Display the sum - sum stored in ebx at this point
  call				crlf
   mDisplayString	offset outro_2
  mov				int_temp,				ebx
  push				offset sum_string									; correct string could be used for the average and sum, but would need to be cleared each time if it was. This seemed cleaner, and was easier to debug
  push				offset temp_string
  push				int_temp
  call				writeVal

  ; Display/calculate the truncated average
  call				crlf
  mDisplayString	offset outro_3
  mov				eax,					ebx
  mov				ebx,					NUMUSERINPUT
  mov				edx,					0
  cdq
  idiv				ebx

  mov				int_temp,				eax
  push				offset average_string
  push				offset temp_string
  push				int_temp
  call				writeVal

  ; Display goodbye
  call				crlf
  mDisplayString	offset outro_4


  Invoke ExitProcess,0	; exit to operating system
main ENDP


; -- readVal --
; Procedure to read user input as a string and check if it can be a int, and then convert it to one and store it
; preconditions:  prompt_1, prompt_2, buffer, int_temp, user_input, and the current segment of int_array have been initialized and pushed
; postconditions: None
; receives:  prompt_1, prompt_2, buffer, int_temp, user_input, and int_array have been initialized and pushed
; returns: an int version of user_input is passed into the position of int_aray that is passed, user_input contains the string version of the input
readVal PROC
  local			bufferloc:DWORD, temp_val:SDWORD, stringLength: DWORD, neg_number: SDWORD
  push			eax
  push			ebx
  push			edx
  push			esi
  push			edi
  push			ecx
  
  mov			ebx,			[ebp + 8]			; prompt_1
  jmp			_FirstRun
  
  _InvalidInput:
  mov			ebx,			[ebp + 12]			; prompt_2 if invalid input was entered

  _FirstRun:
  mov			eax,			[ebp + 16]			; buffer
  mov			bufferloc,		eax
  
  ;mov			eax,			12
  mGetString	ebx,			bufferloc, 13
  mov			stringLength,	eax					
  ;cmp			stringLength,	11					; Not sure if this would've been considered the "hard way" for validating, so commented it out
  ;JG			_InvalidInput



  mov			[ebp + 24],		edx					; setting user_input string to be what was inputted

  mov			ebx,			0
  
  cld												; clearing direction flag
  mov			esi,			[ebp + 24]			; esi is now the user_input string
  mov			edi,			[ebp + 28]			; edi is now the passed offset for converted input
  mov			ecx,			stringLength		; making ecx the size of the string for the loop
  mov			eax,			0					; clearing eax, and therefore AL
  mov			edx,			0					; clear edx to store current int in progress 
  ;mov			temp_val,		0					; clear temp_val to store current int in progress, so we dont get a weird over
  mov			neg_number,		1
  mov			ebx,			0
  _ConversionLoop:
 LODSB												; place first byte from user_input (esi) into AL
  
  cmp			al,				43
  JNE			_not_plus
  cmp			ecx,			stringLength
  JNE			_InvalidInput
  dec			ecx		
  JMP			_ConversionLoop


  _not_plus:

  cmp			al,				45
  JNE			_not_minus
  cmp			ecx,			stringLength
  JNE			_InvalidInput
  mov			neg_number,			-1
  dec			ecx
  JMP			_ConversionLoop
  _not_minus:
  cmp			al,				48
  JL			_InvalidInput

  cmp			al,				57
  JG			_InvalidInput
  
  
  imul			edx, 10
  sub 			AL,				48d

  movSX			ebx,			AL
  add			edx,			ebx
  
  dec			ecx
  cmp			ecx,			0					; probably could've been done with some form of rep, but i thought this was cleaner, since all other conditions to jump back use a jump
  JG			_ConversionLoop
  
  jmp			_final_checks 


  _final_checks:
  imul			edx,			neg_number
  mov			temp_val,		edx
  cmp			neg_number,		-1
  JE			_negative_check
  mov			temp_val,		edx
  cmp			edx,2147483647						; checking if the number is larger than what can be stored in a SDWORD
  JA			_InvalidInput
  JMP			_valid
  
  _negative_check:
  mov			ecx,		edx
  imul			ecx,		neg_number
  cmp			ecx,		2147483648
  JA			_InvalidInput

  _valid:
  mov			[edi],	edx

  pop			ecx
  pop			edi
  pop			esi
  pop			edx
  pop			ebx
  pop			eax

  ret		24
readVal ENDP

; -- writeVal --
; Procedure to convert int to string and print it using mDisplayString
; preconditions:  int_temp, offset correct_string (or some other string of size 13), and offset temp_string (or some other string of size 13) have been initialized and pushed, with int_temp containing an int. The 2 passed strings must be cleared out before successive calls to writeVal if reused
; postconditions: displays passed number, after converting it to a string
; receives: int_temp, correct_string, and temp_string (or 2 other strings of length 13 that are cleared)
; returns: None
writeVal PROC
  Local		sign:BYTE, temp:DWORD
  push			esi
  push			eax
  push			ebx
  push			edx
  push			edi
  push			ecx

  mov			sign,		"+"
  mov			edi,		[ebp + 12]			; edi stores the destination for the string
  mov			eax,		[ebp + 8]			; eax is now the int_temp value passed by value
  mov			ecx,		0
  cmp			eax,		0					; check if negative, will need to preappend sign then
  JGE			_int_to_string_loop
  imul			eax,		-1
  mov			sign,		"-"
  
  

  _int_to_string_loop:
    CLD											; setting flag to be clear (i know there is probably a way to do this using STD, and not having to reverse the string at the end, but I couldnt figure it out)
	mov			ebx,			10
	mov			edx,			0
	div			ebx
	mov			temp,			eax				; storing eax in temp, so AL can be used in STOSB
	mov			eax,			edx
	add 		AL,				48d
	inc			ecx
	STOSB	
	mov			eax,			temp
	cmp			eax,			0
	JG			_int_to_string_loop

  cmp			sign,		"-"
  JNE			_pos							; jump if sign is poitive 
  mov			al,			sign				; adding the sign, whether + or - to the number 
  STOSB
  inc		ecx
  _pos:
  mov		edx,		[ebp+12]


  ; reversing string to be normal left-to-right readable (code modified from exploration 1 - lower level programming)
  
  mov    esi,			[ebp+12]							
  add    esi,			ecx
  dec	 esi			
  mov    edi,			[ebp+16]
  
  mov	ebx,			ecx




  _revLoop:		
	STD
	LODSB
	CLD
	STOSB
	dec	ecx		
	cmp	ecx, 0
	JG	_revLoop

  mov			edx,		[ebp+16]
  mDisplayString	[ebp+16]

  pop			ecx
  pop			edi
  pop			edx
  pop			ebx
  pop			eax
  pop			esi
  ret 12
writeVal ENDP


  END main

 