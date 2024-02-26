import pytest
from gameoflife import GameOfLife, Cell
#attention faire le test avec un input précis 
#Avec un input  000
#               010
#               000

# Test pour vérifier l'initialisation correcte d'une cellule
def test_cell_initialization():
    cell = Cell(0, 0, True)
    assert cell.alive == True
    assert cell.x == 0
    assert cell.y == 0

# Test pour vérifier le chargement d'un état à partir d'un fichier
def test_load_state():
    gol = GameOfLife(3, 3)
    # Utilisation d'un raw string pour le chemin Windows
    gol.load_state(r"C:\INFO\gameoflife\input.txt")
    # Vérifiez que l'état chargé correspond à ce qui est attendu
    assert not gol.cells[0][0].alive
    assert not gol.cells[0][1].alive
    assert gol.cells[1][1].alive  # La cellule centrale doit être vivante

# Test pour vérifier la mise à jour de l'état du jeu
def test_update_state():
    gol = GameOfLife(3, 3)
    gol.load_state(r"C:\INFO\gameoflife\input.txt")
    gol.update_state()
    # Après une mise à jour, toutes les cellules doivent être mortes car une seule cellule vivante ne peut survivre seule.
    for row in gol.cells:
        for cell in row:
            assert not cell.alive

# Test pour vérifier la sauvegarde de l'état du jeu
def test_save_state(tmp_path):
    gol = GameOfLife(3, 3)
    gol.load_state(r"C:\INFO\gameoflife\input.txt")
    file_path = tmp_path / "output.txt"
    gol.save_state(file_path)
    with open(file_path, "r") as file:
        lines = file.readlines()
        # Assurez-vous que le contenu sauvegardé correspond à l'état attendu après chargement initial
        assert lines[1].strip() == "010", "Le fichier sauvegardé ne correspond pas à l'état attendu"
