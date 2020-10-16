import requests

import tqdm


class ApiQueryError(Exception):
    pass


class QueryInitialResponses:
    """
    Access the initial cultural habits of customers.
    """

    def __init__(self, api_key, form_id):
        self.api_key = api_key
        self.form_id = form_id

    def query_page(self, nb_items_per_page=1000, before=None):
        """
        Typeform responses are stored in pages of {nb_items_per_page} items each (except possibly the last one).
        Query a page of responses, possibly submitted until a specified time.
        Args:
            nb_items_per_page (int): number of items in each page
            before (string): limit request to responses submitted before a request token.

        Returns:
            requests.models.Response: a requests response.
        """
        request_url = f"https://api.typeform.com/forms/{self.form_id}/responses?page_size={nb_items_per_page}"
        if before is not None:
            request_url += f"&before={before}"

        result = requests.get(
            request_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if result.status_code != 200:
            raise ApiQueryError(
                f"Error {result.status_code} when querying typeform API on {self.form_id} form."
            )
        return result

    def query_all(self, nb_items_per_page=1000):
        """
        Query all typeform responses.
        Args:
            nb_items_per_page (int): the number of items per page chosen to query typeform responses.
        Returns:
            List[dict]: the list of responses.
        """
        data = self.query_page(nb_items_per_page=nb_items_per_page).json()
        items = data["items"]
        nb_items = len(items)

        progress_bar = tqdm.tqdm(total=data["page_count"])

        while nb_items > 0:
            new_items = self.query_page(
                nb_items_per_page=nb_items_per_page, before=items[-1].get("token")
            ).json()["items"]
            items.extend(new_items)

            nb_items = len(new_items)
            progress_bar.update(1)

        return items
