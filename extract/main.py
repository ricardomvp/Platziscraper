import requests
import bs4
import logging
import datetime
import csv
import os.path

PLATZI='https://www.platzi.com'

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

def main():

    csv_headers=['Category',
                 'Carrer Description',
                 'Carrer Route',
                 'Course Description',
                 'course Route',
                 '# of Reviews',
                 'Comment',
                 'Author',
                 #'Question',
                 'Time w/o response',
                 #'# of responses'
                 ]

    now=datetime.datetime.now() .strftime('%y_%m_%d')
    if os.path.exists('PlatziScraper_{datetime}.csv'.format(datetime=now))==False:
        save_data(csv_headers)

    ##################categories
    categories_link = parsing('',".HomeCategories-items")
    for category in categories_link[0]:
        row_data=[]
        logger.info('Get Category at: ' + PLATZI + category.a['href'])#category
        row_data.append(category.a['href'])#category
        ##################careers
        carrers_link= parsing(category.a['href'],".CarrersItem")
        carrers = [carrer for carrer in carrers_link]
        for carrer in carrers:
            logger.info('Carrer desc:\t' + carrer.h2.string) #carrer description
            logger.info('Carrer root:\t' + PLATZI + carrer['href']) #carrer root
            row_data.append(carrer.h2.string)#carrer description
            row_data.append(carrer['href'])#carrer root
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
                    row_data.remove(course_description)#course description
                    row_data.remove(course_root)#course root
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
                    row_data.append(course_root.replace('cursos','clases'))#course root
                    ##################content
                    comment(course_root,course_root)
                    row_data.remove(course_description)#course description
                    row_data.remove(course_root.replace('cursos','clases'))#course root
                    break
                #################new_page_version#################
            row_data.remove(carrer.h2.string)#carrer description
            row_data.remove(carrer['href'])#carrer root
            break
        #break
        row_data.append(category.a['href'])#category
    logger.info('DONE!!!!!!!  :)')


def parsing(link, clase):
    response = requests.get(PLATZI + link)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup.select(clase)


def comment(course,row_data):
    course_review = parsing(course.replace('cursos','clases') + '?filter=unanswered',".BannerTop-ranking")
    discussion = parsing(course.replace('cursos','clases') + '?filter=unanswered',".Discussion")
    try:
        review=course_review[0]
        #print('Finding Debug. Review: {}'.format(review))
        if review:
            review=review.a.text[18:].replace(')','')
        else:
            review='No reviews'

        logger.info('\t\t\t\t# de reviews=' + review) #number of reviews by course
        for comment in discussion:
            logger.info('Get comment:\t\t\t' + comment.a['href']) #comment number
            ##logger.info('\t\t\t' + comment.select('.DiscussionMeta-username')[0]['href']) #Author
            ##logger.info('\t\t\t' + comment.select('.DiscussionContent-text')[0].text) #question
            ##logger.info('\t\t\t' + comment.select('.DiscussionMeta-date')[0].text) #time wo response
            ##logger.info('\t\t\t' + comment.select('.amount\n')[0].text) #responses

            row_data.append(review)#number of reviews by course
            row_data.append(PLATZI + comment.a['href'])#comment number
            row_data.append(comment.select('.DiscussionMeta-username')[0]['href'])#Author
            #row_data.append(comment.select('.DiscussionContent-text')[0].text)#question
            row_data.append(comment.select('.DiscussionMeta-date')[0].text)#time wo response
            #row_data.append(comment.select('.amount\n')[0].text)#number of responses
            #print(row_data)
            save_data(row_data)
            logger.info('\t\t\t\t\tData saved!\n')
            row_data.remove(review)#number of reviews by course
            row_data.remove(PLATZI + comment.a['href'])#comment number
            row_data.remove(comment.select('.DiscussionMeta-username')[0]['href'])#Author
            #row_data.remove(comment.select('.DiscussionContent-text')[0].text)#question
            row_data.remove(comment.select('.DiscussionMeta-date')[0].text)#time wo response
            #row_data.remove(comment.select('.amount\n')[0].text)#number of responses
            #break
    except IndexError:
        logger.info('Oops! exclusive Course')


def save_data(*row_data):
    now=datetime.datetime.now() .strftime('%y_%m_%d')
    out_file_name='PlatziScraper_{datetime}.csv'.format(datetime=now)
    with open(out_file_name,mode='a+') as f:
        writer=csv.writer(f)
        for row in row_data:
            writer.writerow(row)

if __name__=='__main__':
    main()
