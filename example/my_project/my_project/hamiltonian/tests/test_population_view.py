"""Test for the population view
"""
from typing import Set

from django.test import TestCase

from bs4 import BeautifulSoup


class PopulationViewTestCase(TestCase):
    """Test for the population view.

    Test clicks through the population page to generate a script which is
    run and checked if the desired classes are generated.
    """

    @staticmethod
    def get_soup(response) -> BeautifulSoup:
        """Returns soup for response object
        """
        return BeautifulSoup(response.content, "html.parser")

    def test_01_page_status(self):
        """Tests if the page is found
        """
        response = self.client.get("/populate/")
        self.assertEqual(response.status_code, 200)

    def get_model_choices(self, soup) -> Set[str]:
        """Locates form on page, selcts name select and extracts options.
        """
        form = soup.find("form")
        self.assertIsNotNone(form)

        select = form.find("select", attrs={"name": "model"})
        self.assertIsNotNone(select)

        return {el.text for el in select.find_all("option")}

    def test_02_choices_present(self):
        """Tests if the inital form has the right choices.
        """
        soup = self.get_soup(self.client.get("/populate/"))
        self.assertEqual(
            self.get_model_choices(soup),
            {"Contact[Hamiltonian]", "Coulomb[Hamiltonian]", "Eigenvalue[Base]"},
        )

    def test_03_pick_eiegenvalue(self):
        """Selects the eigenvalue option for the form
        """
        self.test_01_page_status()  # needed to initialize cookies
        response = self.client.post(
            "/populate/",
            data={"model": ["Eigenvalue[Base]"], "parse_tree": ["on"]},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        soup = self.get_soup(response)
        self.assertEqual(
            self.get_model_choices(soup),
            {"Contact[Hamiltonian]", "Coulomb[Hamiltonian]"},
        )

    def test_04_pick_hamiltonian(self) -> str:
        """Selcts Hamiltonian after choosing an eigenvalue

        Checks if the code block is present.

        Returns:
            The code block.
        """
        self.test_03_pick_eiegenvalue()  # needed to preselct on previous step
        response = self.client.post(
            "/populate/",
            data={"model": ["Contact[Hamiltonian]"], "parse_tree": ["on"]},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        code = self.get_soup(response).find("pre", attrs={"id": "population-code"})
        self.assertIsNotNone(code)

        return code.text

    def test_05_generated_script(self):
        """Follows the call chain and tests the generated script.

        The generated script is filled out with data, dumped to file and run.
        After the run, the tables are checked if the objects where created.
        """
        code = self.test_04_pick_hamiltonian()
        expected_code = r"""
from my_project.hamiltonian.models import Contact as hamiltonian_Contact
from my_project.hamiltonian.models import Eigenvalue as hamiltonian_Eigenvalue

hamiltonian, created = hamiltonian_Contact.objects.get_or_create(
	n_sites=, # Number of sites in one spatial dimension
	spacing=, # The lattice spacing between sites
	c=, # Interaction parameter of th the Hamiltonian. Implements a contact interaction.
	tag=, # (Optional) User defined tag for easy searches
)

hamiltonian_eigenvalue, created = hamiltonian_Eigenvalue.objects.get_or_create(
	hamiltonian=hamiltonian, # Matrix for which the eigenvalue has been computed.
	n_level=, # The nth eigenvalue extracted in ascending order.
	value=, # The value of the eigenvalue
	tag=, # (Optional) User defined tag for easy searches
)
"""
        self.assertEqual(code, expected_code)
