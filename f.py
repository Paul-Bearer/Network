# place an ! when the post is in Liked post

# liked_post = ['Red', 'Spaghetti']
# all_posts = ['Red', 'Spaghetti', 'Blue', 'Pizza']


# for post in all_posts:
#     print(post)
#     for l_post in liked_post:
#         if l_post == post:
#             print("!")
# liked_post = [1,4]
# all_posts = [1,2,3,4,5]

# for post in all_posts:
#     print(post)
#     if post in liked_post:
#         print('!')

from django.core.paginator import Paginator

objects = ['john', 'paul', 'george', 'ringo', 'star']
# p will print something that is not 100% understandable 
# the second parameter that Paginator takes is how many 'objects' we want displayed on the page
p = Paginator(objects, 2)
count = p.count  # will count the number of items in a list

pages = p.num_pages # will count the number of pages


for i in p.page_range:
    print(i)




# project predictions

# would best practice be creating a function and calling it where I need it or repeat pagination for index, profile, and following?

# paginator(objects, 10)

# work in index\

# all posts will be the variable used, will replace objects in example above

# main feed, profile page, and following page needs pagination 