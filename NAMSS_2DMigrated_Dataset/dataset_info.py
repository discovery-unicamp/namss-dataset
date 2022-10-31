import os
from functools import lru_cache

@lru_cache(maxsize=None)
def get_survey_split(): 
    return {
	'b-01-75-at'	:	'train',
	'b-01-80-at'	:	'train',
	'b-01-81-at'	:	'train',
	'b-01-82-at'	:	'train',
	'b-01-83-at'	:	'train',
	'b-01-84-at'	:	'train',
	'b-01-88-at'	:	'train',
	'b-01-95-la'	:	'discarded',
	'b-02-77-at'	:	'train',
	'b-02-79-at'	:	'train',
	'b-02-80-at'	:	'train',
	'b-02-81-ar'	:	'train',
	'b-02-82-at'	:	'train',
	'b-02-84-at'	:	'train',
	'b-03-75-at'	:	'train',
	'b-03-80-ar'	:	'train',
	'b-03-81-at'	:	'train',
	'b-03-82-at'	:	'train',
	'b-04-80-at'	:	'train',
	'b-04-81-at'	:	'train',
	'b-04-82-at'	:	'train',
	'b-04-83-at'	:	'train',
	'b-05-81-at'	:	'train',
	'b-05-83-at'	:	'train',
	'b-06-76-at'	:	'train',
	'b-06-79-at'	:	'train',
	'b-06-82-at'	:	'train',
	'b-07-76-at'	:	'train',
	'b-07-78-ak'	:	'train',
	'b-07-81-at'	:	'train',
	'b-07-83-at'	:	'train',
	'b-08-75-at'	:	'train',
	'b-08-78-at'	:	'train',
	'b-08-83-at'	:	'train',
	'b-09-75-at'	:	'train',
	'b-09-81-at'	:	'train',
	'b-10-80-at'	:	'train',
	'b-10-81-at'	:	'train',
	'b-10-82-at'	:	'train',
	'b-11-77-at'	:	'train',
	'b-11-78-at'	:	'train',
	'b-11-82-at'	:	'train',
	'b-11-88-at'	:	'train',
	'b-12-77-at'	:	'train',
	'b-13-76-at'	:	'train',
	'b-13-78-at'	:	'train',
	'b-14-77-at'	:	'discarded',
	'b-15-77-ak'	:	'train',
	'b-15-79-at'	:	'train',
	'b-15-87-ar'	:	'train',
	'b-16-76-at'	:	'train',
	'b-16-77-at'	:	'train',
	'b-17-77-at'	:	'train',
	'b-23-81-ar'	:	'train',
	'b-25-77-ak'	:	'train',
	'b-28-75-at'	:	'train',
	'b-29-76-at'	:	'train',
	'b-30-82-ar'	:	'train',
	'b-32-84-ar'	:	'train',
	'b-33-77-ak'	:	'train',
	'b-59-82-ar'	:	'train',
	'b-60-82-ar'	:	'train',
	'h-14-79-sc'	:	'train',
	'h-17-79-sc'	:	'train',
	'h-18-79-sc'	:	'train',
	'j-1-88-sc'	:	'train',
	'l-09-11-ga-mcs'	:	'train',
	'l-11-11-bs-mcs'	:	'test',
	'l-12-82-wg'	:	'train',
	'l-4-90-sc'	:	'discarded',
	'p-02-10-cc'	:	'discarded',
	'p1-13-la-green-canyon'	:	'discarded',
	'p1-13-la-walker-ridge'	:	'discarded',
	't-03-11-at'	:	'discarded',
	't-06-12-at'	:	'discarded',
	't-21-10-at'	:	'discarded',
	't-39-12-at'	:	'discarded',
	'v-1-09-ca'	:	'discarded',
	'v-1-11-ca'	:	'discarded',
	'w-1-70-sc'	:	'train',
	'w-1-79-cb'	:	'valid',
	'w-10-78-sc'	:	'train',
	'w-10-79-bs'	:	'test',
	'w-12-79-eg'	:	'train',
	'w-13-77-sc'	:	'train',
	'w-13-79-ar'	:	'train',
	'w-14-76-sf'	:	'valid',
	'w-14-79-wg'	:	'train',
	'w-15-79-bs'	:	'discarded',
	'w-16-76-sf'	:	'valid',
	'w-16-77-bs'	:	'test',
	'w-17-77-ar'	:	'discarded',
	'w-17-79-nc'	:	'valid',
	'w-18-75-np'	:	'test',
	'w-18-77-ar'	:	'discarded',
	'w-19-78-ar'	:	'discarded',
	'w-2-70-sc'	:	'train',
	'w-2-75-wg'	:	'train',
	'w-2-91-wy'	:	'discarded',
	'w-20-79-ar'	:	'train',
	'w-21-80-bs'	:	'test',
	'w-22-79-np'	:	'valid',
	'w-23-81-sc'	:	'train',
	'w-25-80-ar'	:	'train',
	'w-26-80-wg'	:	'train',
	'w-26-80-wo'	:	'test',
	'w-27-81-cs'	:	'train',
	'w-29-80-wo'	:	'test',
	'w-3-75-sc'	:	'train',
	'w-3-79-cb'	:	'valid',
	'w-3-91-wy'	:	'discarded',
	'w-30-81-cs'	:	'train',
	'w-30-81-sc'	:	'train',
	'w-31-81-bs'	:	'test',
	'w-31-81-sc'	:	'train',
	'w-32-82-cc'	:	'train',
	'w-33-81-ar'	:	'train',
	'w-33-82-sc'	:	'train',
	'w-34-82-aa'	:	'train',
	'w-34-82-mb'	:	'valid',
	'w-35-82-nc'	:	'valid',
	'w-36-83-sc'	:	'train',
	'w-37-84-sc'	:	'train',
	'w-38-83-sc'	:	'train',
	'w-39-85-wo'	:	'test',
	'w-4-74-sc'	:	'train',
	'w-4-77-sa'	:	'test',
	'w-4-82-nc'	:	'valid',
	'w-40-80-ak'	:	'train',
	'w-40-85-sc'	:	'train',
	'w-5-75-sc'	:	'train',
	'w-5-77-ar'	:	'discarded',
	'w-5-82-sc'	:	'train',
	'w-50-70-cs'	:	'train',
	'w-6-75-nc'	:	'valid',
	'w-6-78-bs'	:	'test',
	'w-6-85-sc'	:	'train',
	'w-62-77-ar'	:	'discarded',
	'w-67-82-wg'	:	'train',
	'w-8-78-ar'	:	'discarded',
	'w-9-78-nc'	:	'valid',
	'w-9-79-ar'	:	'train',
	'w-95-92-sa'	:	'test'
    }


@lru_cache(maxsize=None)
def get_discarded_lines():
    discarded_lines_raw = \
    """b-01-75-at/A-125A-D.segy
    b-01-75-at/A-133A-D.segy
    b-01-75-at/A-157B-D.segy
    b-01-75-at/A-227-D.segy
    b-01-75-at/A-231-D.segy
    b-01-75-at/A-235-D.segy
    b-01-95-la/95-ahc-asp-1a.segy
    b-01-95-la/95-ahc-asp-2.segy
    b-01-95-la/95-ahc-asp-3.segy
    b-01-95-la/95-ahc-asq-1.segy
    b-01-95-la/95-ahc-asq-2.segy
    b-01-95-la/95-ahc-ats-1a.segy
    b-01-95-la/95-ahc-ats-2.segy
    b-01-95-la/ahc95-ahd-1.segy
    b-01-95-la/ahc95-ats-1.segy
    b-01-95-la/bpxat-95-0001.segy
    b-01-95-la/lt1-2983.segy
    b-02-77-at/BP-102-D.segy
    b-02-82-at/PR82-131-D.segy
    b-02-82-at/PR82-170-D.segy
    b-02-82-at/PR82-182-D.segy
    b-02-82-at/PR82-191-D.segy
    b-02-82-at/PR82-198-D.segy
    b-02-82-at/PR82-213-D.segy
    b-02-82-at/PR82-219A-D.segy
    b-02-82-at/PR82-230-D.segy
    b-02-82-at/PR82-232-D.segy
    b-02-82-at/PR82-X227C-D.segy
    b-02-82-at/PR82-X233B-D.segy
    b-02-82-at/PR82-X253-D.segy
    b-02-82-at/PR82-X265-D.segy
    b-02-82-at/PR82-X265A-D.segy
    b-02-82-at/PR82-X273-D.segy
    b-03-81-at/PR81-10-D-D.segy
    b-03-81-at/PR81-13-D.segy
    b-03-81-at/PR81-133-D.segy
    b-03-81-at/PR81-141A-D.segy
    b-03-81-at/PR81-151-D.segy
    b-03-81-at/PR81-151A-D.segy
    b-03-81-at/PR81-155-D.segy
    b-03-81-at/PR81-159-D.segy
    b-03-81-at/PR81-16-D.segy
    b-03-81-at/PR81-16A-D.segy
    b-03-81-at/PR81-191-D.segy
    b-03-81-at/PR81-259A-D.segy
    b-03-81-at/PR81-261-D.segy
    b-03-81-at/PR81-281-D.segy
    b-03-81-at/PR81-281A-D.segy
    b-03-81-at/PR81-289-D.segy
    b-03-81-at/PR81-303-D.segy
    b-03-81-at/PR81-317A-D.segy
    b-03-81-at/PR81-365-D.segy
    b-03-81-at/PR81-367-D.segy
    b-03-81-at/PR81-51-D.segy
    b-03-81-at/PR81-53-D.segy
    b-03-81-at/PR81-59-D.segy
    b-03-81-at/PR81-73-D.segy
    b-03-81-at/PR81-83A-D.segy
    b-03-81-at/PR81-93-D.segy
    b-03-81-at/PR81-93A-D.segy
    b-03-82-at/19490-D.segy
    b-03-82-at/19491-D.segy
    b-03-82-at/19499-D.segy
    b-03-82-at/19510-D.segy
    b-03-82-at/19511-D.segy
    b-03-82-at/19512-D.segy
    b-03-82-at/19513-D.segy
    b-03-82-at/19514-D.segy
    b-03-82-at/19515-D.segy
    b-03-82-at/19516-D.segy
    b-03-82-at/19518-D.segy
    b-03-82-at/19519-D.segy
    b-03-82-at/19520-D.segy
    b-03-82-at/19521-D.segy
    b-03-82-at/19522-D.segy
    b-03-82-at/19523-D.segy
    b-03-82-at/19749-D.segy
    b-03-82-at/19750-D.segy
    b-03-82-at/19751-D.segy
    b-03-82-at/29520-D.segy
    b-04-82-at/17985-D.segy
    b-04-82-at/18012-D.segy
    b-04-82-at/18036-D.segy
    b-04-82-at/18062-D.segy
    b-04-82-at/18067-D.segy
    b-04-82-at/18072-D.segy
    b-04-82-at/18074-D.segy
    b-04-82-at/18078-D.segy
    b-04-82-at/18162-D.segy
    b-04-82-at/28034-D.segy
    b-05-83-at/MMA-148-D.segy
    b-05-83-at/MMA-149-D.segy
    b-05-83-at/MMA-152-D.segy
    b-05-83-at/MSA-267-D.segy
    b-07-81-at/CSA81-10-D_migr.segy
    b-07-81-at/CSA81-11-D_migr.segy
    b-07-81-at/CSA81-12B-D_migr.segy
    b-07-81-at/CSA81-2-D_migr.segy
    b-07-81-at/CSA81-4-D_migr.segy
    b-07-81-at/CSA81-5-D_migr.segy
    b-07-81-at/CSA81-6-D_migr.segy
    b-07-81-at/CSA81-8-D_migr.segy
    b-07-81-at/CSA81-9-D_migr.segy
    b-08-83-at/BC-01-D.segy
    b-08-83-at/BC-04-D.segy
    b-08-83-at/BC-06-D.segy
    b-08-83-at/BC-07-D.segy
    b-08-83-at/BC-08-D.segy
    b-08-83-at/BC-09-D.segy
    b-08-83-at/BC-10-D.segy
    b-08-83-at/BC-12-D.segy
    b-08-83-at/BC-13-D.segy
    b-08-83-at/BC-14-D.segy
    b-08-83-at/BC-19-D.segy
    b-08-83-at/BC-21-D.segy
    b-08-83-at/BC-24-D.segy
    b-08-83-at/BC-26-D.segy
    b-08-83-at/BC-43-D.segy
    b-08-83-at/BC-44-D.segy
    b-10-81-at/A388-AN-16765-D_migr.segy
    b-10-81-at/A388-AN-16767-D_migr.segy
    b-10-81-at/A388-AN-16769-D_migr.segy
    b-10-81-at/A388-AN-16809-D_migr.segy
    b-10-81-at/A388-AN-16810-D_migr.segy
    b-10-82-at/G82-015-D.segy
    b-10-82-at/G82-022A-D.segy
    b-10-82-at/G82-025-D.segy
    b-10-82-at/G82-030-D.segy
    b-10-82-at/G82-034-D.segy
    b-10-82-at/G82-035-D.segy
    b-10-82-at/G82-075-D.segy
    b-10-82-at/G82-099-D.segy
    b-10-82-at/G82-123-D.segy
    b-10-82-at/G82-139_migr.segy
    b-11-77-at/MA-115-D.segy
    b-11-77-at/MA-147-D.segy
    b-11-77-at/MA-159-D.segy
    b-11-77-at/MA-163-D.segy
    b-11-77-at/MA-165-D.segy
    b-11-77-at/MA-171-D.segy
    b-11-77-at/MA-175-D.segy
    b-11-77-at/MA-185-D.segy
    b-11-77-at/MA-193-D.segy
    b-14-77-at/NJ-771-3-D.segy
    b-14-77-at/NJ-776-4-D.segy
    b-14-77-at/NJ-776A-4-D.segy
    b-14-77-at/NJ-779-2-D.segy
    b-15-77-ak/SP77-004_2__SP-9.sgy
    b-15-77-ak/SP77-014__SP-3.sgy
    b-15-77-ak/SP77-016_2__SP-7.sgy
    b-15-77-ak/SP77-017_1__SP-7.sgy
    b-15-77-ak/SP77-025__SP-4.sgy
    b-15-77-ak/SP77-028_1__SP-8.sgy
    b-15-77-ak/SP77-037__SP-11.sgy
    b-15-77-ak/SP77-047__SP-5.sgy
    b-15-77-ak/SP77-055__SP-5.sgy
    b-15-77-ak/SP77-057__SP-5.sgy
    b-15-77-ak/SP77-088__SP-6.sgy
    b-15-77-ak/SP77-090__SP-6.sgy
    b-15-77-ak/SP77-096__SP-10.sgy
    h-17-79-sc/4331__7-12127.1.sgy
    h-17-79-sc/4509__7-12105.1.sgy
    h-18-79-sc/4426.mig.sgy
    h-18-79-sc/4560.mig.sgy
    l-4-90-sc/l4mig118.sgy
    l-4-90-sc/l4mig120.sgy
    p-02-10-cc/1021-stbd-mig.sgy
    p-02-10-cc/1039-stbd-mig.sgy
    p-02-10-cc/1084-stbd-mig.sgy
    p-02-10-cc/1138-stbd-mig.sgy
    p-02-10-cc/1174-stbd-mig.sgy
    p-02-10-cc/1210-stbd-mig.sgy
    p-02-10-cc/1219-stbd-mig.sgy
    p-02-10-cc/1246-stbd-mig.sgy
    p-02-10-cc/1291-stbd-mig.sgy
    p-02-10-cc/1309-stbd-mig.sgy
    p-02-10-cc/1363-stbd-mig.sgy
    p-02-10-cc/1390-stbd-mig.sgy
    p-02-10-cc/1435-stbd-mig.sgy
    p-02-10-cc/1453-stbd-mig.sgy
    p-02-10-cc/1489-stbd-mig.sgy
    p-02-10-cc/1516-stbd-mig.sgy
    p-02-10-cc/1525-stbd-mig.sgy
    p-02-10-cc/1543-stbd-mig.sgy
    p-02-10-cc/1561-stbd-mig.sgy
    p-02-10-cc/1570-stbd-mig.sgy
    p-02-10-cc/1579-stbd-mig.sgy
    p-02-10-cc/1633-stbd-mig.sgy
    p-02-10-cc/1723-stbd-mig.sgy
    p-02-10-cc/1732-stbd-mig.sgy
    p-02-10-cc/1750-stbd-mig.sgy
    p-02-10-cc/1831-stbd-mig.sgy
    p-02-10-cc/1840-stbd-mig.sgy
    p-02-10-cc/1876-stbd-mig.sgy
    p-02-10-cc/1912-stbd-mig.sgy
    p-02-10-cc/1957-stbd-mig.sgy
    p-02-10-cc/1966-stbd-mig.sgy
    p-02-10-cc/1975-stbd-mig.sgy
    p-02-10-cc/1993-stbd-mig.sgy
    p1-13-la-green-canyon/GC125-mig.sgy
    p1-13-la-green-canyon/GC127a-mig.sgy
    p1-13-la-green-canyon/GC217-mig.sgy
    p1-13-la-green-canyon/GC225a-mig.sgy
    p1-13-la-green-canyon/GC229-mig.sgy
    p1-13-la-green-canyon/GC261-mig.sgy
    p1-13-la-green-canyon/GC265-mig.sgy
    p1-13-la-green-canyon/GC321a-mig.sgy
    p1-13-la-walker-ridge/WR227-migration.sgy
    p1-13-la-walker-ridge/WR228-migration.sgy
    p1-13-la-walker-ridge/WR230-migration.sgy
    p1-13-la-walker-ridge/WRCSEMA-migration.sgy
    t-03-11-at/T2011.19t.mig.1500.sgy
    t-03-11-at/T2011.20.mig.1500.sgy
    t-06-12-at/T2012.July.105.tstat.mig.sgy
    t-06-12-at/T2012.July.111.tstat.mig.sgy
    t-06-12-at/T2012.July.113b.tstat.mig.sgy
    t-21-10-at/T2010.1100.mig.1500.sgy
    t-21-10-at/T2010.1103.mig.1500.sgy
    t-21-10-at/T2010.111.mig.1500.sgy
    t-39-12-at/T2012.Oct.06b.tstat.mig.sgy
    t-39-12-at/T2012.Oct.10.tstat.mig.sgy
    v-1-09-ca/ML-20.sgy
    v-1-09-ca/ML-36A.sgy
    v-1-09-ca/ML-39.sgy
    v-1-09-ca/ML-40.sgy
    v-1-09-ca/ML-46.sgy
    v-1-09-ca/ML-52.sgy
    v-1-09-ca/ML-56.sgy
    v-1-09-ca/ML-63.sgy
    v-1-09-ca/ML-67.sgy
    v-1-09-ca/ML-70.sgy
    v-1-11-ca/ML-104.sgy
    v-1-11-ca/ML-124.sgy
    v-1-11-ca/ML-127.sgy
    v-1-11-ca/ML-130.sgy
    v-1-11-ca/ML-132.sgy
    v-1-11-ca/ML-139.sgy
    v-1-11-ca/ML-145.sgy
    v-1-11-ca/ML-151.sgy
    v-1-11-ca/ML-156.sgy
    w-15-79-bs/WNS-205A_1_623871.sgy
    w-15-79-bs/WNS-205A_387872.sgy
    w-15-79-bs/WNS-209A_611332.sgy
    w-15-79-bs/WNS-211A_484029.sgy
    w-15-79-bs/WNS-213A_625448.sgy
    w-15-79-bs/WNS-215A_272356.sgy
    w-15-79-bs/WNS-217A_230277.sgy
    w-15-79-bs/WNS-221A_490581.sgy
    w-15-79-bs/WNS-225A_647443.sgy
    w-15-79-bs/WNS-253A_433611.sgy
    w-15-79-bs/WNS-254A_1_623746.sgy
    w-15-79-bs/WNS-255A_399775.sgy
    w-15-79-bs/WNS-258A_656491.sgy
    w-15-79-bs/WNS-259A_262530.sgy
    w-15-79-bs/WNS-260A_340989.sgy
    w-15-79-bs/WNS-260A_637134.sgy
    w-15-79-bs/WNS-262A_1_474923.sgy
    w-15-79-bs/WNS-262A_1_660508.sgy
    w-15-79-bs/WNS-262A_2_635276.sgy
    w-15-79-bs/WNS-262A_481488.sgy
    w-15-79-bs/WNS-263A_253012.sgy
    w-15-79-bs/WNS-265A_102090.sgy
    w-15-79-bs/WNS-266A_478301.sgy
    w-15-79-bs/WNS-267A_253350.sgy
    w-15-79-bs/WNS-274A_492228.sgy
    w-15-79-bs/WNS-276A_352355.sgy
    w-15-79-bs/WNS-276A_393091.sgy
    w-16-77-bs/WNS-005A_462681.sgy
    w-16-77-bs/WNS-008A_585449.sgy
    w-16-77-bs/WNS-010A_1_437716.sgy
    w-16-77-bs/WNS-010A_44097.sgy
    w-16-77-bs/WNS-011A_484970.sgy
    w-16-77-bs/WNS-012A_1_368627.sgy
    w-16-77-bs/WNS-012A_358391.sgy
    w-16-77-bs/WNS-012A_433205.sgy
    w-16-77-bs/WNS-015A_344106.sgy
    w-16-77-bs/WNS-016A_347738.sgy
    w-16-77-bs/WNS-017A_286758.sgy
    w-16-77-bs/WNS-018A_1_296980.sgy
    w-16-77-bs/WNS-019A_448012.sgy
    w-16-77-bs/WNS-021A_250592.sgy
    w-16-77-bs/WNS-023A_462907.sgy
    w-16-77-bs/WNS-024A_358627.sgy
    w-16-77-bs/WNS-024A_601169.sgy
    w-16-77-bs/WNS-025A_278287.sgy
    w-16-77-bs/WNS-027A_369570.sgy
    w-16-77-bs/WNS-029A_398015.sgy
    w-16-77-bs/WNS-031A_261882.sgy
    w-16-77-bs/WNS-033A_487306.sgy
    w-16-77-bs/WNS-035A_488938.sgy
    w-16-77-bs/WNS-039A_476837.sgy
    w-16-77-bs/WNS-039A_486176.sgy
    w-16-77-bs/WNS-041A_488887.sgy
    w-16-77-bs/WNS-043A_488844.sgy
    w-16-77-bs/WNS-045A_486531.sgy
    w-16-77-bs/WNS-049A_474752.sgy
    w-16-77-bs/WNS-051A_297785.sgy
    w-16-77-bs/WNS-053A_369233.sgy
    w-17-77-ar/WB-001_705587.sgy
    w-17-77-ar/WB-009_705587.sgy
    w-17-77-ar/WB-013_729198.sgy
    w-17-77-ar/WB-015_729198.sgy
    w-17-77-ar/WB-017_729144.sgy
    w-17-77-ar/WB-037_729144.sgy
    w-17-77-ar/WB-078_728931.sgy
    w-17-77-ar/WB-080_728931.sgy
    w-17-77-ar/WB-094_784523.sgy
    w-17-77-ar/WB-096_784523.sgy
    w-17-77-ar/WB-098_784523.sgy
    w-17-77-ar/WB-100_784523.sgy
    w-17-77-ar/WB-104_784523.sgy
    w-17-77-ar/WB-106_784523.sgy
    w-17-77-ar/WB-108_784523-1.sgy
    w-17-77-ar/WB-108_784523.sgy
    w-17-77-ar/WB-110_784523.sgy
    w-17-77-ar/WB-118_725517.sgy
    w-18-75-np/WR-001A_1__220158.sgy
    w-18-75-np/WR-001A_2__206209.sgy
    w-18-75-np/WR-001A_3__249999.sgy
    w-18-75-np/WR-001A_3__252047.sgy
    w-18-75-np/WR-001A_4_5__236463.sgy
    w-18-75-np/WR-001A_4_5__586070.sgy
    w-18-75-np/WR-001_3_4__245335.sgy
    w-18-75-np/WR-001__596180.sgy
    w-18-75-np/WR-004__574766.sgy
    w-18-75-np/WR-006__413580.sgy
    w-18-75-np/WR-008__116150.sgy
    w-18-75-np/WR-010__245369.sgy
    w-18-75-np/WR-010__419990.sgy
    w-18-75-np/WR-012__247817.sgy
    w-18-75-np/WR-014__531897.sgy
    w-18-75-np/WR-016__123039.sgy
    w-18-75-np/WR-018__589294.sgy
    w-18-75-np/WR-018__591987.sgy
    w-18-75-np/WR-022__325434.sgy
    w-18-75-np/WR-024__406294.sgy
    w-18-75-np/WR-024__555526.sgy
    w-18-75-np/WR-026__593971.sgy
    w-18-77-ar/WB-020_729144.sgy
    w-18-77-ar/WB-024_729144.sgy
    w-18-77-ar/WB-026_729144.sgy
    w-18-77-ar/WB-028_729144.sgy
    w-18-77-ar/WB-030_729144.sgy
    w-18-77-ar/WB-032_729144.sgy
    w-18-77-ar/WB-034_729144.sgy
    w-18-77-ar/WB-036_729144.sgy
    w-18-77-ar/WB-038_729126.sgy
    w-18-77-ar/WB-040_729126.sgy
    w-18-77-ar/WB-042_729126.sgy
    w-18-77-ar/WB-044_729126.sgy
    w-18-77-ar/WB-048_729126.sgy
    w-18-77-ar/WB-052_729126.sgy
    w-18-77-ar/WB-054_729126.sgy
    w-18-77-ar/WB-056_729126.sgy
    w-18-77-ar/WB-058_729126.sgy
    w-18-77-ar/WB-060_728931.sgy
    w-18-77-ar/WB-066_728931.sgy
    w-18-77-ar/WB-142_725517.sgy
    w-18-77-ar/WB-144_725517.sgy
    w-18-77-ar/WB-146_725517.sgy
    w-18-77-ar/WB-148_725517.sgy
    w-18-77-ar/WB-152_725517.sgy
    w-18-77-ar/WB-158_725517.sgy
    w-18-77-ar/WB-160_725517.sgy
    w-18-77-ar/WB-166_725517.sgy
    w-18-77-ar/WB-170_725544.sgy
    w-18-77-ar/WB-174_725544.sgy
    w-18-77-ar/WB-176_725544.sgy
    w-18-77-ar/WB-500_725544.sgy
    w-19-78-ar/WB-737_782124.sgy
    w-19-78-ar/WB-739_782124.sgy
    w-19-78-ar/WB-741_782124.sgy
    w-19-78-ar/WB-743_782124.sgy
    w-19-78-ar/WB-747_782124.sgy
    w-19-78-ar/WB-749_782124-1.sgy
    w-19-78-ar/WB-749_782124-2.sgy
    w-19-78-ar/WB-749_782124.sgy
    w-19-78-ar/WB-751_782124-1.sgy
    w-19-78-ar/WB-751_782124.sgy
    w-19-78-ar/WB-753_782124.sgy
    w-19-78-ar/WB-784_782124.sgy
    w-19-78-ar/WB-794_782124.sgy
    w-19-78-ar/WB-798_782124.sgy
    w-19-78-ar/WB-812_910353.sgy
    w-19-78-ar/WB-820_910353.sgy
    w-19-78-ar/WB-822_910353.sgy
    w-19-78-ar/WB-824_910353.sgy
    w-19-78-ar/WB-826_910353.sgy
    w-19-78-ar/WB-828_910353.sgy
    w-19-78-ar/WB-830_910353.sgy
    w-19-78-ar/WB-832_910353-1.sgy
    w-19-78-ar/WB-832_910353.sgy
    w-19-78-ar/WB-834_910353.sgy
    w-19-78-ar/WB-836_910353.sgy
    w-19-78-ar/WB-838_910353.sgy
    w-19-78-ar/WB-840_910353.sgy
    w-19-78-ar/WB-842_910353.sgy
    w-19-78-ar/WB-844_910353.sgy
    w-19-78-ar/WB-846_910353.sgy
    w-19-78-ar/WB-848_978374.sgy
    w-19-78-ar/WB-850_978374.sgy
    w-19-78-ar/WB-852_978374.sgy
    w-19-78-ar/WB-854_978374.sgy
    w-19-78-ar/WB-856_978374.sgy
    w-19-78-ar/WB-858_978374.sgy
    w-19-78-ar/WB-860_978374.sgy
    w-19-78-ar/WB-862_978374.sgy
    w-19-78-ar/WB-864_978374.sgy
    w-19-78-ar/WB-866_978374.sgy
    w-19-78-ar/WB-870_978374.sgy
    w-19-78-ar/WB-874_978374.sgy
    w-19-78-ar/WB-880_978374.sgy
    w-19-78-ar/WB-933_978374.sgy
    w-2-91-wy/grb91_1a.sgy
    w-2-91-wy/grb91_4_.sgy
    w-2-91-wy/grb91_5_.sgy
    w-2-91-wy/grb91_6_.sgy
    w-2-91-wy/grb91_7_.sgy
    w-2-91-wy/grb91_7x.sgy
    w-3-91-wy/grb91_10.sgy
    w-3-91-wy/grb91_11.sgy
    w-3-91-wy/grb91_12.sgy
    w-3-91-wy/grb91_13.sgy
    w-3-91-wy/grb91_14.sgy
    w-3-91-wy/grb91_15.sgy
    w-3-91-wy/grb91_8_.sgy
    w-3-91-wy/grb91_9_.sgy
    w-34-82-aa/WSA-213_123962.sgy
    w-34-82-aa/WSA-226_102633.sgy
    w-40-80-ak/80-01.sgy
    w-40-80-ak/80-07C.sgy
    w-40-80-ak/80-08.sgy
    w-40-80-ak/EP-31.sgy
    w-5-77-ar/WB-007_1-3__994790.sgy
    w-5-77-ar/WB-007__994790.sgy
    w-5-77-ar/WB-016A__994790.sgy
    w-5-77-ar/WB-019__994790.sgy
    w-5-77-ar/WB-021_2__994790.sgy
    w-5-77-ar/WB-021__994790.sgy
    w-5-77-ar/WB-022A_1__994790.sgy
    w-5-77-ar/WB-022A__994790.sgy
    w-5-77-ar/WB-023__994790.sgy
    w-5-77-ar/WB-024A__994790.sgy
    w-5-77-ar/WB-025__994790.sgy
    w-5-77-ar/WB-027__994790.sgy
    w-5-77-ar/WB-028A__994790.sgy
    w-5-77-ar/WB-029__994790.sgy
    w-5-77-ar/WB-031__994790.sgy
    w-5-77-ar/WB-033_1-2__994790.sgy
    w-5-77-ar/WB-033__994790.sgy
    w-5-77-ar/WB-035__994790.sgy
    w-5-77-ar/WB-038A__994790.sgy
    w-5-77-ar/WB-040A__994790.sgy
    w-5-77-ar/WB-042A__994790.sgy
    w-5-77-ar/WB-044A__994790.sgy
    w-5-77-ar/WB-064A__994790.sgy
    w-5-77-ar/WB-066A__922434.sgy
    w-5-77-ar/WB-068A__922434.sgy
    w-5-77-ar/WB-072A__922434.sgy
    w-5-77-ar/WB-076A__922434.sgy
    w-5-77-ar/WB-120__922434.sgy
    w-5-77-ar/WB-122__922434.sgy
    w-5-77-ar/WB-124__922434.sgy
    w-5-77-ar/WB-126__922434.sgy
    w-5-77-ar/WB-128__922434.sgy
    w-5-77-ar/WB-130__922434.sgy
    w-5-77-ar/WB-132__922434.sgy
    w-5-77-ar/WB-134__922434.sgy
    w-5-77-ar/WB-136__922434.sgy
    w-5-77-ar/WB-138__922434.sgy
    w-5-77-ar/WB-200__922434.sgy
    w-5-77-ar/WB-201__922434.sgy
    w-5-77-ar/WB-202__922434.sgy
    w-5-77-ar/WB-203__922434.sgy
    w-5-77-ar/WB-204__922434.sgy
    w-5-77-ar/WB-205__922434.sgy
    w-5-77-ar/WB-206__922434.sgy
    w-5-77-ar/WB-207__922434.sgy
    w-5-77-ar/WB-208__922434.sgy
    w-5-77-ar/WB-209__922434.sgy
    w-5-77-ar/WB-210__922434.sgy
    w-5-77-ar/WB-211__922434.sgy
    w-5-77-ar/WB-213__993988.sgy
    w-5-77-ar/WB-214__993988.sgy
    w-5-77-ar/WB-215__993988.sgy
    w-5-77-ar/WB-216__975951.sgy
    w-5-77-ar/WB-217__975951.sgy
    w-5-77-ar/WB-218__975951.sgy
    w-5-77-ar/WB-219__975951.sgy
    w-5-77-ar/WB-220__975951.sgy
    w-5-77-ar/WB-221__975951.sgy
    w-5-77-ar/WB-222__975951.sgy
    w-5-77-ar/WB-602A__975951.sgy
    w-5-77-ar/WB-604A__975951.sgy
    w-5-77-ar/WB-606A__975951.sgy
    w-5-77-ar/WB-608A__975951.sgy
    w-6-85-sc/SB85-10_501151.sgy
    w-6-85-sc/SB85-12_501151.sgy
    w-6-85-sc/SB85-13_501151.sgy
    w-6-85-sc/SB85-16_500968.sgy
    w-6-85-sc/SB85-17_500968.sgy
    w-6-85-sc/SB85-18_500968.sgy
    w-6-85-sc/SB85-19_500968.sgy
    w-6-85-sc/SB85-20_500968.sgy
    w-6-85-sc/SB85-21_500968.sgy
    w-6-85-sc/SB85-23_500968.sgy
    w-6-85-sc/SB85-24_500968.sgy
    w-6-85-sc/SB85-28_501421.sgy
    w-6-85-sc/SB85-29_501421.sgy
    w-6-85-sc/SB85-33_501421.sgy
    w-6-85-sc/SB85-35_501421.sgy
    w-6-85-sc/SB85-36_501421.sgy
    w-6-85-sc/SB85-37_501421.sgy
    w-6-85-sc/SB85-39_501421.sgy
    w-6-85-sc/SB85-40_501421.sgy
    w-62-77-ar/B-01X__500307.sgy
    w-62-77-ar/B-21__500838.sgy
    w-62-77-ar/B-27A__500838.sgy
    w-62-77-ar/B-27__500838.sgy
    w-62-77-ar/B-35__500838.sgy
    w-62-77-ar/SP77-001__500240.sgy
    w-62-77-ar/SP77-002__SP-9.sgy
    w-62-77-ar/SP77-003A__SP-9.sgy
    w-62-77-ar/SP77-004_2__SP-9.sgy
    w-62-77-ar/SP77-004__SP-9.sgy
    w-62-77-ar/SP77-005B__500240.sgy
    w-62-77-ar/SP77-005C_1__500240.sgy
    w-62-77-ar/SP77-005C__500308.sgy
    w-62-77-ar/SP77-005_1__SP-3.sgy
    w-62-77-ar/SP77-005__SP-9.sgy
    w-62-77-ar/SP77-006__SP-3.sgy
    w-62-77-ar/SP77-007__SP-3.sgy
    w-62-77-ar/SP77-008__SP-12.sgy
    w-62-77-ar/SP77-009A__500305.sgy
    w-62-77-ar/SP77-010_1__SP7710.sgy
    w-62-77-ar/SP77-010__SP7710.sgy
    w-62-77-ar/SP77-012__SP-3.sgy
    w-62-77-ar/SP77-013A__500307.sgy
    w-62-77-ar/SP77-013__500307.sgy
    w-62-77-ar/SP77-014_1__SP-7.sgy
    w-62-77-ar/SP77-014__SP-3.sgy
    w-62-77-ar/SP77-015__SP-7.sgy
    w-8-78-ar/WB-700_772168.sgy
    w-8-78-ar/WB-702_772168.sgy
    w-8-78-ar/WB-705_772168-1.sgy
    w-8-78-ar/WB-705_772168-2.sgy
    w-8-78-ar/WB-705_772168.sgy
    w-8-78-ar/WB-707_772168.sgy
    w-8-78-ar/WB-717_772168.sgy
    w-8-78-ar/WB-719_1_772168.sgy
    w-8-78-ar/WB-719_772168.sgy
    w-8-78-ar/WB-723_981334.sgy
    w-8-78-ar/WB-725_981334-1.sgy
    w-8-78-ar/WB-729_981334.sgy
    w-8-78-ar/WB-733_981334.sgy
    w-8-78-ar/WB-742_981334.sgy
    w-8-78-ar/WB-744_981334-1.sgy
    w-8-78-ar/WB-744_981334.sgy
    w-8-78-ar/WB-746A_910555.sgy
    w-8-78-ar/WB-748_910555.sgy
    w-8-78-ar/WB-752_910555-1.sgy
    w-8-78-ar/WB-752_910555.sgy
    w-8-78-ar/WB-756_910555.sgy
    w-8-78-ar/WB-760_910555.sgy
    w-8-78-ar/WB-764_910555.sgy
    w-8-78-ar/WB-772_910555.sgy
    w-8-78-ar/WB-786_910555-1.sgy
    w-8-78-ar/WB-786_910555.sgy
    w-8-78-ar/WB-790_724121-1.sgy
    w-8-78-ar/WB-790_724121.sgy
    w-8-78-ar/WB-792_741419-1.sgy
    w-8-78-ar/WB-792_741419.sgy
    w-8-78-ar/WB-796_724121-1.sgy
    w-8-78-ar/WB-796_724121-2.sgy
    w-8-78-ar/WB-796_724121.sgy
    w-8-78-ar/WB-800_724121.sgy
    w-8-78-ar/WB-814_1_724121.sgy
    w-8-78-ar/WB-814_724121.sgy
    w-8-78-ar/WB-818_724121-1.sgy
    w-8-78-ar/WB-818_724121.sgy
    w-8-78-ar/WB-901_1_952885-1.sgy
    w-8-78-ar/WB-901_1_952885-2.sgy
    w-8-78-ar/WB-901_1_952885.sgy
    w-8-78-ar/WB-901_703052.sgy
    w-8-78-ar/WB-903_703052-1.sgy
    w-8-78-ar/WB-903_703052.sgy
    w-8-78-ar/WB-905_703052-1.sgy
    w-8-78-ar/WB-905_703052.sgy
    w-8-78-ar/WB-907_952885-1.sgy
    w-8-78-ar/WB-907_952885-2.sgy
    w-8-78-ar/WB-907_952885-3.sgy
    w-8-78-ar/WB-907_952885.sgy
    w-8-78-ar/WB-911_1_952885.sgy
    w-8-78-ar/WB-911_952885.sgy
    w-8-78-ar/WB-912_1_952885.sgy
    w-8-78-ar/WB-913A_703052.sgy
    w-8-78-ar/WB-913_703052-1.sgy
    w-8-78-ar/WB-913_703052.sgy
    w-8-78-ar/WB-914_952885.sgy
    w-8-78-ar/WB-915_703052-1.sgy
    w-8-78-ar/WB-915_703052.sgy
    w-8-78-ar/WB-916_952885-1.sgy
    w-8-78-ar/WB-916_952885.sgy
    w-8-78-ar/WB-917_952885.sgy
    w-8-78-ar/WB-919_975951-1.sgy
    w-8-78-ar/WB-919_975951.sgy
    w-8-78-ar/WB-921_703052.sgy
    w-8-78-ar/WB-922_975951.sgy
    w-8-78-ar/WB-923_952885.sgy
    w-8-78-ar/WB-923_979000.sgy
    w-8-78-ar/WB-924_975951.sgy
    w-8-78-ar/WB-925_952885.sgy
    w-8-78-ar/WB-926_952885.sgy
    w-8-78-ar/WB-927_952885-1.sgy
    w-8-78-ar/WB-927_952885.sgy
    w-8-78-ar/WB-928_952885.sgy
    w-8-78-ar/WB-930_952885.sgy
    w-8-78-ar/WB-931_703052.sgy
    w-8-78-ar/WB-937_952885.sgy
    w-8-78-ar/WB-939_749985.sgy
    w-8-78-ar/WB-939_952885.sgy
    w-8-78-ar/WB-943_703052.sgy""".split('\n')

    discarded_lines = dict()
    for line in discarded_lines_raw:
        survey, line = line.strip().split('/')
        line = os.path.splitext(line)[0]
        if survey not in discarded_lines:
            discarded_lines[survey] = set([line])
        else:
            discarded_lines[survey].add(line)

    return discarded_lines
