import requests
import bs4
import logging


PLATZI='https://www.platzi.com'

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

def main():
    ##################categories
    categories_link = parsing('',".HomeCategories-items")
    for category in categories_link[0]:
        logger.info('Get Category at: ' + PLATZI + category.a['href'])#category


        ##################careers
        carrers_link= parsing(category.a['href'],".CarrersItem")
        carrers = [carrer for carrer in carrers_link]
        for carrer in carrers:
            logger.info('Carrer desc:\t' + carrer.h2.string) #carrer description
            logger.info('Carrer root:\t' + PLATZI + carrer['href']) #carrer root

            ##################curses
            route = parsing(carrer['href'],".route-item")
            if route:
                #################old_page_version#################
                course_link=[course for course in route]
                for course in course_link:
                    logger.info('Course desc:\t\t' + course.h4.string) #course description
                    logger.info('course root:\t\t' + PLATZI + course.a['href'].replace('cursos','clases')+ '?filter=unanswered') #course root
                    ##################content
                    comment(course.a['href'])
                    break
                #################old_page_version#################
            else:
                #################new_page_version#################
                course_link = parsing(carrer['href'],".CareerCourseItem")
                for course in course_link:
                    logger.info('Course desc:\t\t' + course.h5.string) #course description
                    logger.info('course root:\t\t' + course.a['href'])#course root
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
        logger.info('\t\t\t\t# de reviews=' + review) #number of reviews by course
        for comment in discussion:
            logger.info('Get comment:\t\t\t' + comment.a['href']) #comment number
            ##logger.info('\t\t\t' + comment.select('.DiscussionMeta-username')[0]['href']) #Author
            ##logger.info('\t\t\t' + comment.select('.DiscussionContent-text')[0].text) #question
            ##logger.info('\t\t\t' + comment.select('.DiscussionMeta-date')[0].text) #time wo response
            ##logger.info('\t\t\t' + comment.select('.amount\n')[0].text) #responses


            ################## DATA TO BE INTRODUCED IN THE DB ##################
            #print('**' + PLATZI + category.a['href'] + '**')#category
            #print('\t' + carrer.h2.string) #carrer description
            #print('\t' + carrer['href']) #carrer root

            #################old_page_version#################
            #print('\t\t' + course.h4.string) #course description
            #print('\t\t' + course.a['href'].replace('cursos','clases')) #course root
            #################old_page_version#################
            #################new_page_version#################
            ##print(course.h5.string) #course description
            ##print(course.a['href'])#course root
            #################new_page_version#################

            #print('\t\t# de reviews= ' + review) #number of reviews by course
            #print('\t\t\t' + comment.a['href']) #comment number
            #print('\t\t\t' + comment.select('.DiscussionMeta-username')[0]['href']) #Author
            #print('\t\t\t' + comment.select('.DiscussionContent-text')[0].text) #question
            #print('\t\t\t' + comment.select('.DiscussionMeta-date')[0].text) #time wo response
            #print('\t\t\t' + comment.select('.amount\n')[0].text) #responses
            ################## DATA TO BE INTRODUCED IN THE DB ##################

    except IndexError:
        logger.info('Oops! exclusive Course')


if __name__=='__main__':
    main()
