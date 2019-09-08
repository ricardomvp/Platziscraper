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
        row_data=[]
        logger.info('Get Category at: ' + PLATZI + category.a['href'])#category
        row_data.append(PLATZI + category.a['href'])#category

        ##################careers
        carrers_link= parsing(category.a['href'],".CarrersItem")
        carrers = [carrer for carrer in carrers_link]
        for carrer in carrers:
            logger.info('Carrer desc:\t' + carrer.h2.string) #carrer description
            logger.info('Carrer root:\t' + PLATZI + carrer['href']) #carrer root

            row_data.append(carrer.h2.string)#carrer description
            row_data.append(PLATZI + carrer['href'])#carrer root

            ##################curses
            route = parsing(carrer['href'],".route-item")
            if route:
                #################old_page_version#################
                course_link=[course for course in route]
                for course in course_link:
                    course_description= course.h4.string
                    course_root= course.a['href']
                    logger.info('Course desc:\t\t' + course_description) #course description
                    logger.info('course root:\t\t' + PLATZI + course_root.replace('cursos','clases') + '?filter=unanswered') #course root
                    row_data.append(course_description)#course description
                    row_data.append(course_root)#course root
                    ##################content
                    comment(course_root,row_data)

                    break
                #################old_page_version#################
            else:
                #################new_page_version#################
                course_link = parsing(carrer['href'],".CareerCourseItem")
                for course in course_link:
                    course_description= course.h5.string
                    course_root= course.a['href']
                    logger.info('Course desc:\t\t' + course_description) #course description
                    logger.info('course root:\t\t' + PLATZI + course_root.replace('cursos','clases')+ '?filter=unanswered') #course root
                    row_data.append(course_description)#course description
                    row_data.append(course_root)#course root
                    ##################content
                    comment(course_root,course_root)

                    break
                #################new_page_version#################

            break
        break


def parsing(link, clase):
    response = requests.get(PLATZI + link)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup.select(clase)


def comment(course,row_data):
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

            row_data.append(review)#number of reviews by course
            row_data.append(comment.a['href'])#comment number
            row_data.append(comment.select('.DiscussionMeta-username')[0]['href'])#Author
            row_data.append(comment.select('.DiscussionContent-text')[0].text)#question
            row_data.append(comment.select('.DiscussionMeta-date')[0].text)#time wo response
            row_data.append(comment.select('.amount\n')[0].text)#number of esponses

            print(row_data)
            break


    except IndexError:
        logger.info('Oops! exclusive Course')

if __name__=='__main__':
    main()
