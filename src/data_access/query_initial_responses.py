import requests

import tqdm


class ApiQueryError(Exception):
    pass


class QueryInitialResponses:
    """
    Access the initial cultural habits of customers.
    """

    def __init__(self, env, api_key, form_dict=None):
        self.env = env
        if form_dict is not None:
            self.form_dict = form_dict
        else:
            self.form_dict = {
                "prod": "Oqu7Ag",
                "testing": "T8rurj",
                "staging": "OoEtVb"
            }
        self.api_key = api_key

    def query_page(self, nb_items_per_page, page_index):
        """
        Typeform responses are stored in pages of {nb_items_per_page} items each (except possibly the last one).
        Query the page of index {page_index} of these typeform responses.
        Args:
            nb_items_per_page (int): number of items in each page
            page_index (int): index of the page queried

        Returns:
            requests.models.Response: a requests response.
        """
        res = requests.get(
            f"https://api.typeform.com/forms/{self.form_dict[self.env]}/responses?page_size={nb_items_per_page}&page={page_index}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if res.status_code != 200:
            raise ApiQueryError(
                f"Error {res.status_code} when querying typeform API on {self.form_dict[self.env]} form.")
        return res

    def query_all(self, nb_items_per_page=30, last_page=None):
        """
        Query all typeform responses.
        Args:
            nb_items_per_page (int): the number of items per page chosen to query typeform responses.
            last_page (int): last page to query (if None, query all pages).
        Returns:
            List[dict]: the list of responses.
        """
        data = self.query_page(nb_items_per_page, 1)
        total_pages = data.json()['page_count']

        items = data.json()['items']

        if last_page is None:
            last_page = total_pages + 1

        for page_index in tqdm.tqdm(
                range(2, last_page)
        ):
            items.extend(
                self.query_page(nb_items_per_page, page_index).json()['items']
            )
        return items
