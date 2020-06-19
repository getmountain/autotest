import entity_pb2

03 entitydesc= entity_pb2.entity_desc()

04 entitydesc.entity_id=1

05 entitydesc.entity_name='haha'

06 

07 #create proto  

15 entitydesc_str=entitydesc.SerializeToString()  

16 print entitydesc_str    

17 print '----'







18 #read

19 entityattr2 = entity_pb2.entity_attr()

20 entityattr2.ParseFromString(entity_attr_str)

21 print entityattr2.attr_id    

22 print entityattr2.attribute.decode('utf-8').encode('gbk')

23 for i in entityattr2.value:

24    print i

25    

26 print '----'

27 entitydesc2= entity_pb2.entity_desc()

28 entitydesc2.ParseFromString(entitydesc_str)    

29 print entitydesc2.entity_id

30 #repeated entity_attr attributes，由于是repeated需要遍历

31 for oneatt in entitydesc2.attributes:

32    print oneatt.attr_id

33    for i in oneatt.value:

34        print i
