from scraper import scrape_pages


def main():
    for result in scrape_pages(total_pages=5):
        print(result)


if __name__ == "__main__":
    main()