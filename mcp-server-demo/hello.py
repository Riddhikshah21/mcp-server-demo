from mcp.server.fastmcp import FastMCP
import os 

# Create an MCP server
mcp = FastMCP("AI Sticky Notes")

# Notes where mcp server will have access to 
NOTES_FILE = os.path.join(os.path.dirname(__file__), "ai_notes.txt")

def check_file_exists():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'w') as f: #creates a new file 
            f.write("")

# Decorator - design pattern in python that allows to add funtionality to an existing object
# Always add datatype in the function definition and docstring for providing additional information of the tool 
@mcp.tool()
def add_note(message: str) -> str: 
    '''
    Append a new note to the sticky note file.

    Args:
        message(str): The note content to be added.

    Returns:
        str: Confirmation message indicating the note was added.  
    '''
    check_file_exists()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note added!"

@mcp.tool()
def read_notes() -> str:
    """
    Read and return the content of the current notes.

    Returns: 
        str: All the notes in a single string separated by a line break. If no notes exist, return a default message. 
    """
    check_file_exists()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
        return content or "No notes yet."
    
@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Read and return the content of the current notes.
    
    Returns: 
        str: All the notes in a single string separated by a line break. If no notes exist, return a default message. 
    """
    check_file_exists()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
        return lines[-1].strip() if lines else "No notes here."
    
@mcp.prompt()
def note_summary() -> str:
    """
    Generate a prompt asking the AI to summarize the notes 

    Returns:
        str: A prompt string that includes a summary of the current notes if found else a message will be shown indicating that. 
    """
    check_file_exists()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    if not content:
        return "There are no notes"
    return f"Summarize the current notes: {content}"