in_str=input()
pre=in_str.split("=")
post_list=list()
ans=""
for i in pre[1]:
    if i.isdigit():
        post_list.append(i)
lhs=list()
if not len(post_list):
    for i in pre[0]:
        if i.isdigit():
            lhs.append(int(i))
    one=str(lhs[0])
    two=str(lhs[1])
    three=str(lhs[0]+lhs[1])
    ans=one+" + "+two+" = "+three
else:
    for i in pre[0]:
        if i.isdigit():
            lhs.append(i)
    one=str(lhs[0])
    # print(post_list[0])
    two=str(int(post_list[0])-int(lhs[0]))
    three=str(post_list[0])
    ans=one+" + "+two+" = "+three
return ans
    

