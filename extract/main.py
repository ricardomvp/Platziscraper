import requests
import bs4

PLATZI='https://www.platzi.com'


def main():
    ##################categories
    categories_link = parsing('',".HomeCategories-items")
    for category in categories_link[0]:
        print('**' + PLATZI + category.a['href'] + '**')#category

        ##################careers
        carrers_link= parsing(category.a['href'],".CarrersItem")
        carrers = [carrer for carrer in carrers_link]
        for carrer in carrers:
            print('\t' + carrer.h2.string) #carrer description
            print('\t' + carrer['href']) #carrer root

            ##################curses
            route = parsing(carrer['href'],".route-item")
            if route:
                #################old_page_version#################
                course_link=[course for course in route]
                for course in course_link:
                    print('\t\t' + course.h4.string) #course description
                    print('\t\t' + course.a['href'].replace('cursos','clases')) #course root
                    ##################content
                    comment(course.a['href'])
                    break
                #################old_page_version#################
            else:
                #################new_page_version#################
                course_link = parsing(carrer['href'],".CareerCourseItem")
                for course in course_link:
                    print(course.h5.string)
                    print(course.a['href'])
                    ##################content
                    comment(course.a['href'])
                    break
                #################new_page_version#################

            break
        break


def parsing(link, clase):
    response = requests.get(PLATZI + link)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup.select(clase)


def comment(course):
    course_review = parsing(course.replace('cursos','clases') + '?filter=unanswered',".BannerTop-ranking")
    discussion = parsing(course.replace('cursos','clases') + '?filter=unanswered',".Discussion")
    try:
        review=course_review[0].a.text[18:].replace(')','')
        print('\t\t# de reviews= ' + review) #number of reviews by course
        for comment in discussion:
            print('\t\t\t' + comment.a['href']) #comment number
            print('\t\t\t' + comment.select('.DiscussionMeta-username')[0]['href']) #Author
            print('\t\t\t' + comment.select('.DiscussionContent-text')[0].text) #question
            print('\t\t\t' + comment.select('.DiscussionMeta-date')[0].text) #time wo response
            print('\t\t\t' + comment.select('.amount\n')[0].text) #responses
    except IndexError:
        print('Oops! exclusive Course')


if __name__=='__main__':
    main()
