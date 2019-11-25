
.mode csv
drop table if exists pnls;
create table pnls("date" date, "sym" text, "country" text, "client" text, "borrow" float, "loan" float, "pnl" float);
.import pnls.csv pnls
