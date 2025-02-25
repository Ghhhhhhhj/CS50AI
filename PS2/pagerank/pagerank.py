import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = dict()
    linked_count = len(corpus[page])
    pages_linked = corpus[page]
    pages_all = corpus.keys()
    page_count = len(corpus)

    if pages_linked:
        for pg in pages_linked:
            model.update({pg: damping_factor / linked_count})
    else:
        for pg in pages_all:
            model.update({pg: 1 / page_count})
        return model
    if pages_all:
        for pg in pages_all:
            if pg in model:
                model[pg] += (1 - damping_factor) / page_count
            else:
                model.update({pg: (1 - damping_factor) / page_count})
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page = random.choice(list(corpus.keys()))
    chosen_pages = {page: 1}
    for _ in range(n - 1):
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model.keys()), list(model.values()))[0]
        if page in chosen_pages.keys():
            chosen_pages[page] += 1
        else:
            chosen_pages.update({page: 1})
    pageranks = dict()
    for page in chosen_pages.keys():
        pageranks.update({page: chosen_pages[page] / n})
    return pageranks




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageranks = dict()
    max_delta = 0.001
    delta = 1
    page_count = len(corpus)

    for page in corpus.keys():
        pageranks.update({page: 1 / page_count})

    while(delta > max_delta):

        delta = 0
        new_pageranks = pageranks.copy()

        for page in corpus.keys():
            pr_sum = 0

            for pg in corpus.keys():
                if corpus[pg]:
                    if page in corpus[pg]:
                        pr_sum += pageranks[pg] / len(corpus[pg])
                else:
                    pr_sum += pageranks[pg] / page_count

            rank = (1 - damping_factor) / page_count + damping_factor * pr_sum
            new_pageranks[page] = rank
            delta = max(delta, abs(rank - pageranks[page])) 

        pageranks = new_pageranks

    return pageranks




if __name__ == "__main__":
    main()
