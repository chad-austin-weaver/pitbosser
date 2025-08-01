1. Visit pitbosser.streamlit.app in browser.
2. Upload .csv file of your own (formatting noted below) or use one of the user_test folder's many files included in the attached .zip folder. (For evaluation purposes, given the combinatorial complexity of the problem, keep the number of games and dealers minimal, around 3-5 game types and 9-12 dealers for a result to be found without significant computational time).
3. Scroll down as the streamlit web app populates with a generated table of assignments, and charts for comparison to that of the average games in the report.

CSV format:
integer_max_relief_tables,game_type0,game_type1,...,gametypeN
integer_#_of_tables_game_type0, integer_#_of_tables_game_type1,...,integer_#_of_tables_game_typeN
dealer0_name,0-1,0-1,...,0-1 [1 representing this line's dealer knowing how to deal game_type0, 1, ... N in place. 0 representing that they do not.]
dealer1_name,0-1,0-1,...,0-1
...
dealerM_name,0-1,0-1,...,0-1

[NOTE: In industry, a "integer_max_relief_tables" value outside of [3-4] would be exceedingly rare.]
[NOTE: The second line will be 'offset' by one left from the corresponding game_types, and leave an empty space in the right-most 'cell' this is okay and handled during processing.]
[NOTE: Given all 0 values in line 2, the default strip game mix will be assigned]

[Currently accepted game_types: blackjack, craps, roulette, 3-card poker, baccarat, mini-baccarat, let it ride, pai gow, pai gow poker, other]

Example:
3,blackjack,roulette,craps,baccarat,other |	[3 relief tables max per dealer, game types are [blackjack,roulette,craps,baccarat,other]]
1,1,1,1,0 				  |	[1 blackjack, 1 roulette, 1 craps, 1 baccarat, 0 other tables.]
"d0",1,0,0,0,0 				  |	[dealer d0 knows blackjack.]
"d1",0,0,1,1,1				  |	[dealer d1 knows craps, baccarat, other.]
"d2",0,0,1,0,0				  |	...
"d3",0,1,1,1,0				  |
"d4",0,1,0,0,0				  |
"d5",0,0,1,0,0				  |
"d6",1,1,0,1,0				  |
"d7",1,1,1,1,1				  |	[dealer d7 knows blackjack, roulette, craps, baccarat, other.]
