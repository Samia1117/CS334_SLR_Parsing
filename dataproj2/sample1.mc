size 40 40
begin
	mouse jerry 10 10 north ;
	clockwise jerry ;
	cat tom 30 30 west ;
	repeat 3
		clockwise tom ;
	end ;
	cat sylvester 30 10 south ;
	hole 20 20 ;
	move jerry ;
	move jerry 19 ;
	move tom 15 ;
	repeat 2
		clockwise jerry ;
	end ;
	move jerry 20 ;
	clockwise tom ;
	move sylvester 10 ;
	move tom 10 ;
	repeat 3
		clockwise tom ;
	end ;
	move tom 10 ;
	move jerry 5 ;
	clockwise tom ;
	repeat 10
		move sylvester ;
		move tom ;
	end ;
halt
	