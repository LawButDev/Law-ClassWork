list1 = [2,5,15,36,47,56,59,78,156,244,268]
list2 = [18,39,42,43,66,69,100]
MergeList = []
i = 0
j = 0
list1.sort()
list2.sort()
while((i < len(list1)) and (j<len(list2))):
    if list1[i]<list2[j]:
        MergeList.append(list1[i]) # append the item from list 1
        i += 1
    else:
        MergeList.append(list2[j]) # append item from list 2
        j += 1

while i < len(list1):
    MergeList.append(list1[i])
    i += 1

while j < len(list2):
    MergeList.append(list2[j])
    j += 1
print(list1)
print(list2)
print(MergeList)
