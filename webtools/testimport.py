from webtools import find_links, check_activity

root = find_links.FindLinks("https://www.ebeactive.pl/")
for i in root:
    print(i)

print('---------------------------------------------------')

root2 = find_links.FindLinks(
    '/home/threaz/Desktop/webtools/html_files/file0_1.html')
for j in root2:
    print(j)

print('---------------------------------------------------')

root3 = check_activity.LinksActivity(
    "/home/threaz/Desktop/webtools/html_files")
for i in root3:
    print(i)
