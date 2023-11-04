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
    # define probabilities as a dictionary
    probability = {}
    
    # that will be linked with damping_factor probability
    page_links = corpus[page]
    
    # loops in damping factor
    available_links = []
    
    # filling the transition model 
    for page in corpus:
        available_links.append(page)
        # initialize dictionary
        probability[page] = 0
    
    for link in page_links:
        probability[link] = (damping_factor) * (1/len(page_links))
        
    for link in available_links:
        probability[link] = probability[link] + ((1-damping_factor) * (1/len(available_links)))
        
    return probability
    

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    created_pages = {}
    # Generating random page
    first_page = random.choice(pages)
    
    # initial probability
    for page in pages:
        created_pages[page] = 0
    
    # update the probability
    created_pages[first_page] = 1/n
    current_probability = transition_model(corpus, first_page, damping_factor)
    
    # sampling process
    for i in range(0, n-1):
        new_page = random.choices(list(current_probability.keys()), list(current_probability.values()), k=1)
        created_pages[new_page[0]] = created_pages[new_page[0]] + 1/n
        current_probability = transition_model(corpus,new_page[0],damping_factor)
        
    return created_pages
    
    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    initial_rank = 1 / N
    pagerank = {page: initial_rank for page in corpus}
    # Define the threshold for convergence
    change_threshold = 0.001

    while True:
        # Initialize a new PageRank dictionary for the next iteration
        new_pagerank = {}

        for page in corpus:
            # Initialize the rank for the current page
            new_rank = (1 - damping_factor) / N
            for linking_page, linked_pages in corpus.items():
                if page in linked_pages:
                    # Update the rank based on the linked pages and damping factor
                    new_rank += damping_factor * pagerank[linking_page] / len(linked_pages)
            # Store the new rank for the current page
            new_pagerank[page] = new_rank

        # Check for convergence by finding the maximum change in PageRank values
        max_change = max(abs(new_pagerank[page] - pagerank[page]) for page in corpus)
        if max_change < change_threshold:
            # If the change is smaller than the threshold, stop iterating
            break

        # Update the PageRank values for the next iteration
        pagerank = new_pagerank

    return pagerank


if __name__ == "__main__":
    main()

 