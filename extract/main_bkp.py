def main():
    ##################categoria
    category_response = requests.get(PLATZI)
    soup = bs4.BeautifulSoup(category_response.text, 'html.parser')
    categories_link = soup.select(".HomeCategories-items")


    for category in categories_link[0]:
        print('**' + PLATZI + category.a['href'] + '**')
        ##################carrera

        carrer_response = requests.get(PLATZI + category.a['href'])
        soup = bs4.BeautifulSoup(carrer_response.text, 'html.parser')
        carrers = soup.select(".CarrersItem")

        carrer_link = [carrer['href'] for carrer in carrers]
        #carrer_description=[carrer.h2 for carrer in carrers]

        #for carrer in carrer_description:
            #print(carrer.string)
        #print('*'*20)
        for carrer in carrer_link:
            print('\t' + carrer)
            ##################curso
            course_response = requests.get(PLATZI + carrer)
            soup = bs4.BeautifulSoup(course_response.text, 'html.parser')
            route = soup.select(".route-item")

            course_link = [course.a for course in route]
            #course_description=[course.h4 for course in route]

            #for course in course_description:
                #print(course.string)
            #print('*'*20)
            for course in course_link:
                print('\t\t' + course['href'].replace('cursos','clases'))
                ##################preguntas

                response = requests.get(PLATZI + course['href'].replace('cursos','clases') + '?filter=unanswered')
                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                discussion = soup.select(".Discussion")
                course_review = soup.select(".BannerTop-ranking")

                review=course_review[0].a.text[18:].replace(')','')
                print('\t\t# de reviews= ' + review)

                for comment in discussion:
                    print('\t\t\t' + comment.a['href'])
                    print('\t\t\t' + comment.select('.DiscussionMeta-username')[0]['href'])
                    print('\t\t\t' + comment.select('.DiscussionContent-text')[0].text)
                    print('\t\t\t' + comment.select('.DiscussionMeta-username')[0]['href'])
                    print('\t\t\t' + comment.select('.DiscussionMeta-date')[0].text)
                    print('\t\t\t' + comment.select('.amount')[0].text)
                    print('\t\t\t' + '*'*20)

                break
            break
        break


if __name__=='__main__':
    main()
