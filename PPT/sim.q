
q1: `time xasc([] 
    time:09:30:00.0+100000?23000000; 
    sym:100000?(enlist `0005.HK); 
    spr: 0.20*((100000?2)+1);
    spr_b1: 0.20*((100000?2)+1);
    spr_a1: 0.20*((100000?2)+1);
    spr_b2: 0.20*((100000?2)+1);
    spr_a2: 0.20*((100000?2)+1);
    bid_1:  59.60+0.20*(100000?5);
    bid_1_vol: 2000*((100000?7)+1);
    bid_2_vol: 12000+2000*(100000?5);
    bid_3_vol: 8000+2000*(100000?5);
    tot_1_vol: 16000+2000*(100000?5);
    tot_2_vol: 26000+2000*(100000?5);
    tot_3_vol: 18000+2000*(100000?5));

q1: update bid_2:bid_1-spr_b1 from q1;
q1: update bid_3:bid_2-spr_b2 from q1;
q1: update ask_1:bid_1+spr from q1;
q1: update ask_2:ask_1+spr_a1 from q1;
q1: update ask_3:ask_2+spr_a2 from q1;
q1: update ask_1_vol: tot_1_vol-bid_1_vol from q1;
q1: update ask_2_vol: tot_2_vol-bid_2_vol from q1;
q1: update ask_3_vol: tot_3_vol-bid_3_vol from q1;
q1: delete spr, spr_b1, spr_a1, spr_b2, spr_a2 from q1;
q1: delete tot_1_vol, tot_2_vol, tot_3_vol from q1;

q2: `time xasc([] 
    time:09:30:00.0+100000?23000000; 
    sym:100000?(enlist `0700.HK); 
    spr: 0.50*((100000?2)+1);
    spr_b1: 0.50*((100000?2)+1);
    spr_a1: 0.50*((100000?2)+1);
    spr_b2: 0.50*((100000?2)+1);
    spr_a2: 0.50*((100000?2)+1);
    bid_1:  336.00+0.50*(100000?5);
    bid_1_vol: 2000*((100000?7)+1);
    bid_2_vol: 12000+2000*(100000?5);
    bid_3_vol: 8000+2000*(100000?5);
    tot_1_vol: 16000+2000*(100000?5);
    tot_2_vol: 26000+2000*(100000?5);
    tot_3_vol: 18000+2000*(100000?5));

q2: update bid_2:bid_1-spr_b1 from q2;
q2: update bid_3:bid_2-spr_b2 from q2;
q2: update ask_1:bid_1+spr from q2;
q2: update ask_2:ask_1+spr_a1 from q2;
q2: update ask_3:ask_2+spr_a2 from q2;
q2: update ask_1_vol: tot_1_vol-bid_1_vol from q2;
q2: update ask_2_vol: tot_2_vol-bid_2_vol from q2;
q2: update ask_3_vol: tot_3_vol-bid_3_vol from q2;
q2: delete spr, spr_b1, spr_a1, spr_b2, spr_a2 from q2;
q2: delete tot_1_vol, tot_2_vol, tot_3_vol from q2;

q3: q1, q2
q3: `time xasc q3

q3: select time, sym, bid_1, ask_1, bid_2, ask_2, bid_3, ask_3, bid_1_vol, ask_1_vol, bid_2_vol, ask_2_vol, bid_3_vol, ask_3_vol from q3;

trades: `time xasc([] 
        time:09:30:00.0+1000?23000000; 
        order_id:1000?1000000000;
        strategy:1000?`stratA`stratB`stratC;
        side:1000?`S`B;
        sym:1000?`0005.HK`0700.HK;
        country:1000?(enlist `HK);
        currency:1000?(enlist `HKD);
        size:200*((1000?20)+1)); 

buys: select from trades where side=`B;
sells: select from trades where side=`S;

buys: aj[`sym`time;buys;q3];
sells: aj[`sym`time;sells;q3];

buys: select time, order_id, strategy, side, sym, country, currency, size, ask_1 from buys;
sells: select time, order_id, strategy, side, sym, country, currency, size, bid_1 from sells;

buys: `time`order_id`strategy`side`sym`country`currency`size`price xcol buys;
sells: `time`order_id`strategy`side`sym`country`currency`size`price xcol sells;

trades: buys, sells;
trades: `time xasc trades;

locates1: `date xasc([] 
         date:2019.09.03 2019.09.04 2019.09.05 2019.09.06;
         sym:4?(enlist `0005.HK);
         country:4?(enlist `HK);
         currency:4?(enlist `HKD);
         tot_quantity: 300000+20000*(4?10);
         confirmed_r: 0.3+(4?30)%100);
locates1: update confirmed_quantity:tot_quantity*confirmed_r from locates1;
locates1: update tot_value:tot_quantity*60 from locates1;
locates1: update confirmed_value:confirmed_quantity*60 from locates1;

locates2: `date xasc([] 
         date:2019.09.03 2019.09.04 2019.09.05 2019.09.06;
         sym:4?(enlist `0700.HK);
         country:4?(enlist `HK);
         currency:4?(enlist `HKD);
         tot_quantity: 500000+30000*(4?10);
         confirmed_r: 0.3+(4?30)%100);
locates2: update confirmed_quantity:tot_quantity*confirmed_r from locates2;
locates2: update tot_value:tot_quantity*360 from locates2;
locates2: update confirmed_value:confirmed_quantity*360 from locates2;

locates3: locates1, locates2;
locates3: select date, sym, country, currency, tot_quantity, confirmed_quantity, tot_value, confirmed_value from locates3;

locates3: `date`sym xasc locates3;


trades: `sym`time xasc trades;
q3: `sym`time xasc q3;
w:-00:00:02.000 00:00:01.000+\:trades `time
trades:wj[w;`sym`time;trades;(q3;(max;`ask_1);(min;`bid_1))];
trades:`time`order_id`strategy`side`sym`country`currency`size`price`max_ask`min_bid xcol trades;
trades:`time xasc trades;
trades: select time, order_id, strategy, side, sym, size, price, max_ask, min_bid from trades;

trades2: update size:neg size from trades where side=`S;
imb: select sum size by sym,interval:900000 xbar time from trades2
