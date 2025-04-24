from Basic_Functions import yesno_loop, choice_num_loop, print_choice, menu_handler
from Basic_Objects import Scene, Object, Player, Tracker, Entity, Goblin

# whatever code you find in this file is not used in the game, it is just for testing purposes
# you can delete it and work on your own code here. for example, as of now I'm
# testing a dialogic tree system that will be used in the game

def dialogue_visited(node: "Dialogue_Node") -> None:
    """Marks the node as visited"""
    node.visited = True

class Dialogue_Tree:
    def __init__(self, name: str, options: list["Dialogue_Node"] = []):
        self.name = name
        self.options = options
    
    def add_option(self, nodes: list["Dialogue_Node"]) -> None:
        """Adds a list of nodes to the tree"""
        for node in nodes:
            self.options.append(node)

    def remove_option(self, node: "Dialogue_Node") -> None:
        """Removes a node from the tree"""
        if node in self.options:
            self.options.remove(node)
        else:
            print(f"Node {node.name} not found in options.")

    def run(self) -> None:
        """Runs the dialogue tree"""
        choices = [node for node in self.options if node.parent is None]
        
        if not choices:
            print("No starting dialogue options available.")
            return
        
        for node in choices:
            if node.visited:
                choices.remove(node)
        
        scene = Scene([])
        while choices:
            scene.choices = []  # Clear previous choices
            for node in choices:
                scene.add_choice(node.text_option)
            choice = menu_handler(scene)
            
            if choice == "exit":
                break
            
            temp_node = None
            for node in choices:
                if node.text_option == choice:
                    temp_node = node
                    break
            
            if temp_node is None:
                print("Invalid choice selected.")
                continue
            
            # Execute the node's function with arguments if provided
            if temp_node.function1:
                temp_node.function1()
            if temp_node.function2:
                temp_node.function2()
            
            print(temp_node.text_response)
            temp_node.visited = True  # Mark node as visited
            choices = temp_node.children  # Move to child nodes
            
            if not choices:
                print("Dialogue ended.")
                break


class Dialogue_Node:
    def __init__(self, name: str, text_option: str, text_response: str,
                 parent: object = None, children: list[object] = [],
                 function1: callable = None, function1_args: list = [],
                 function2: callable = None, function2_args: list = [],
                 visited: bool = False) -> None:
        self.name = name
        self.text_option = text_option
        self.text_response = text_response
        self.parent = parent
        self.children = children
        self.function1 = function1
        self.function2 = function2
        self.visited = visited

    def remove_child(self, node : object) -> None:
        """Removes the node from the tree"""
        if node in self.children:
            self.children.remove(node)
        else:
            print(f"Node {node.name} not found in children.")
    
    def delete(self) -> None:
        """Deletes the node from the tree"""
        if self.parent:
            self.parent.remove_option(self)
        else:
            self.delete()


# Example usage
hero = Player(10, 20, "bob", [])

test1 = Dialogue_Tree("test1", [])

test1_1 = Dialogue_Node(
    name="test1_1",
    text_option="I want to heal",
    text_response="You are healed",
    function1=lambda: hero.loot([1, "CHEESE"]),  # Bind the function to the hero instance
    function2=lambda: dialogue_visited(test1_1),  # Bind the function to the hero instance
)
test1_2 = Dialogue_Node(
    name="test1_2",
    text_option="I want to attack",
    text_response="you attack the goblin ending the conversation",
    visited=False
)
test1.add_option([test1_1, test1_2])
test1.run()
test1.run()
print(hero)