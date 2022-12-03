from arcgis import GIS
import pandas as pd
import shutil, os
#%%
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = GIS(tokens.at['uCOP','URL'])
br_layer_item = gis.content.get('7b8ecfaf5c2b43cba2adfd0a86bbef06')
br_layers = br_layer_item.layers
df=br_layers[0].query(where="apppapercopy = 'Yes'").sdf
flayer = br_layers[0]


existingROE = os.listdir(r"\\nwk-netapp2.nwk.ds.usace.army.mil\MISSIONFILES\MissionProjects\civ\Temporary Roofing\10.0 FMS\Mail_Outs_Ian")
existingROE = [int(s.replace('.pdf','').replace('.docx','').replace('~$','')) for s in existingROE]
df=df.loc[~df.index.isin(existingROE)]

df=df[df['signupsource']=='MCV']

for index, row in df.iterrows():
    try:
        shutil.move(os.path.join(r"C:\Users\M3ECHJJJ\Documents\ArcGIS\Projects\BRMS_SDE\Reports/",str(row['roeidpk'])+'.pdf'),
                    r"\\nwk-netapp2.nwk.ds.usace.army.mil\MISSIONFILES\MissionProjects\civ\Temporary Roofing\10.0 FMS\Mail_Outs_Ian"/",str(row['roeidpk'])+'.pdf')
    except:
        pass



318080
318117
324581
326114
342738
343460
343923
343963
345365
345469
345669
347866
348101
348498
350360
350571
351098
351134
351773
351989
358034
374550
375021
376046
392675
393446
402993
403164
407824
408467
409045
409094
409149
411299
411390
413153
413164
413404
414837
414885
461096
462910
466613
466678
470145
474661
479165
480264
482558
484451
491326
498265
498268
498409
506603
512395
512533
512536
516278
516325
520103
520423
532940
533105
540148
540199
540533
553045
567576
567623
580186
584901
588025
588029
589354
595662
605527
605733
605771
612412
612434
641960
663286
663367
686876
724517
748948
750885
753410
753431
761175
772587
772773
772778
785863
789858
801794
801846
841115
849213
849292
849530
859357
877650
877763
877788
899496
919133
941305
941478
954658
956268
