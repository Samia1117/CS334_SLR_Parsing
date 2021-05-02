
    size 40 60
    begin
      cat charlotte 12 1 west ; // a cat, charlotte, at (12,1) heading west
      mouse 1A 3 10 north ;       // a mouse, 1A, (3,10) heading east 
      hole 9 10 ;                 // a hole at (9,10)
      repeat 3
        move  charlotte ;        // charlotte moves one step west 
	move  1A ;               // 1A moves one step east
      end ;
      clockwise charlotte ;
      clockwise charlotte ;
      clockwise charlotte ;      // charlotte now heading south
      repeat 3
         move 1A ;
	 move charlotte 3 ;
      end ;	 
    halt 
