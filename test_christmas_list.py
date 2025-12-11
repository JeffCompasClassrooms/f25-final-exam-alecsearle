import pytest
from christmas_list import ChristmasList
import os
import pickle

@pytest.fixture
def temp_filename(tmp_path):
    return os.path.join(tmp_path, "test_christmas_list.pkl")

def test_add_item(temp_filename):
    cl = ChristmasList(temp_filename)
    cl.add("Toy Car")
    items = cl.loadItems()
    assert len(items) == 1
    assert items[0]["name"] == "Toy Car"
    assert items[0]["purchased"] == False

def test_check_off_item(temp_filename):
    cl = ChristmasList(temp_filename)
    cl.add("Doll")
    cl.check_off("Doll")
    items = cl.loadItems()
    assert items[0]["purchased"] == True

def test_remove_item(temp_filename):
    cl = ChristmasList(temp_filename)
    cl.add("Puzzle")
    cl.remove("Puzzle")
    items = cl.loadItems()
    assert len(items) == 0

def test_print_list(capsys, temp_filename):
    cl = ChristmasList(temp_filename)
    cl.add("Book")
    cl.add("Game")
    cl.check_off("Book")
    cl.print_list()
    captured = capsys.readouterr()
    assert "[x] Book" in captured.out
    assert "[_] Game" in captured.out

def test_print_empy_list(capsys, temp_filename):
    cl = ChristmasList(temp_filename)
    cl.print_list()
    captured = capsys.readouterr()
    assert captured.out == ""

def test_load_items_nonexistent_file(tmp_path):
    temp_filename = os.path.join(tmp_path, "nonexistent.pkl")
    cl = ChristmasList(temp_filename)
    items = cl.loadItems()
    assert items == []

def test_save_and_load_items(temp_filename):
    cl = ChristmasList(temp_filename)
    test_items = [{"name": "Train", "purchased": False}, {"name": "Ball", "purchased": True}]
    cl.saveItems(test_items)
    loaded_items = cl.loadItems()
    assert loaded_items == test_items

def test_multiple_actions(temp_filename):
    cl = ChristmasList(temp_filename)
    cl.add("Action Figure")
    cl.add("Board Game")
    cl.check_off("Action Figure")
    cl.remove("Board Game")
    items = cl.loadItems()
    assert len(items) == 1
    assert items[0]["name"] == "Action Figure"
    assert items[0]["purchased"] == True

def test_add_duplicate_items(temp_filename):
    cl = ChristmasList(temp_filename)
    cl.add("Sticker")
    cl.add("Sticker")
    items = cl.loadItems()
    assert len(items) == 2
    assert items[0]["name"] == "Sticker"
    assert items[1]["name"] == "Sticker"

def test_check_off_nonexistent_item(temp_filename):
    cl = ChristmasList(temp_filename)
    cl.add("Gloves")
    cl.check_off("Scarf")
    items = cl.loadItems()
    assert items[0]["purchased"] == False