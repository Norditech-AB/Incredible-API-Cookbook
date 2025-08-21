#!/usr/bin/env python3
"""
🐉 AI Dungeon Master - Interactive RPG Adventure
=================================================

The most engaging way to learn function calling! Experience AI-powered storytelling
with real game mechanics through interactive function calling.

🎮 What this demonstrates:
• Interactive user input with dynamic AI responses
• Complex function chaining for game mechanics
• State management across multiple function calls
• Random generation with AI creativity
• Real-time decision making and story branching
• Gamification of function calling concepts

🎯 Game Features:
• Create your character (Warrior, Mage, Rogue)
• Interactive storytelling with meaningful choices
• Dice-based combat system with strategy
• Inventory management and equipment upgrades
• Experience points and character progression
• Random encounters and treasure hunting
• Skill challenges (lockpicking, persuasion, magic)
• Persistent game state (save/load progress)

🎲 Function Calling Powers:
• roll_dice() - Combat, skill checks, random events
• manage_player_stats() - Health, XP, level, gold tracking
• manage_inventory() - Equipment, potions, treasures
• combat_system() - Turn-based battles with monsters
• generate_encounter() - Random events and discoveries
• calculate_experience() - Level progression and rewards
• check_skill() - Skill-based challenge resolution

💡 Why This Is Perfect for Learning:
• Shows function calling in a fun, interactive context
• Demonstrates complex multi-function workflows  
• Users see immediate results from their choices
• Combines AI creativity with structured game mechanics
• Makes abstract concepts tangible through gameplay

🎪 Real-World Applications:
• Interactive chatbots with game-like engagement
• Educational applications with gamification
• Customer service bots with personality
• Training simulations with AI guidance
• Entertainment applications with user agency

Ready to embark on an AI-powered adventure? Let's roll! 🎲✨
"""

import os
import json
import random
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Game state storage
GAME_STATE = {
    "player": {
        "name": "",
        "class": "",
        "level": 1,
        "health": 100,
        "max_health": 100,
        "experience": 0,
        "gold": 50,
        "inventory": ["Health Potion", "Rusty Sword"],
        "location": "Village Tavern",
        "story_progress": "beginning"
    },
    "session_stats": {
        "battles_won": 0,
        "treasures_found": 0,
        "skills_used": 0,
        "dice_rolled": 0
    }
}

def roll_dice(num_dice=1, sides=20, modifier=0, purpose="general"):
    """
    Roll dice for various game purposes with dramatic flair!
    """
    global GAME_STATE
    
    rolls = []
    for _ in range(num_dice):
        roll = random.randint(1, sides)
        rolls.append(roll)
    
    total = sum(rolls) + modifier
    GAME_STATE["session_stats"]["dice_rolled"] += num_dice
    
    # Create dramatic descriptions
    roll_descriptions = {
        20: "🌟 CRITICAL SUCCESS! The dice gods smile upon you!",
        1: "💥 CRITICAL FAILURE! Even heroes have bad days...",
        "high": "🎲 Excellent roll! Fortune favors the bold!",
        "medium": "🎲 Solid roll! You're doing well!",
        "low": "🎲 Challenging roll! But heroes overcome obstacles!"
    }
    
    # Determine result quality
    if 20 in rolls:
        description = roll_descriptions[20]
    elif 1 in rolls:
        description = roll_descriptions[1]
    elif total >= 15:
        description = roll_descriptions["high"]
    elif total >= 10:
        description = roll_descriptions["medium"]
    else:
        description = roll_descriptions["low"]
    
    result = {
        "purpose": purpose,
        "num_dice": num_dice,
        "sides": sides,
        "rolls": rolls,
        "modifier": modifier,
        "total": total,
        "description": description,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    
    print(f"🎲 Rolling {num_dice}d{sides}{'+'+str(modifier) if modifier > 0 else ''} for {purpose}...")
    print(f"🎯 Rolled: {rolls} = {total}")
    print(f"✨ {description}")
    
    return result

def manage_player_stats(action, stat=None, amount=0):
    """
    Manage player statistics (health, experience, gold, level).
    """
    global GAME_STATE
    player = GAME_STATE["player"]
    
    if action == "get_stats":
        stats = {
            "name": player["name"],
            "class": player["class"],
            "level": player["level"],
            "health": f"{player['health']}/{player['max_health']}",
            "experience": player["experience"],
            "gold": player["gold"],
            "location": player["location"]
        }
        print(f"📊 CHARACTER STATS:")
        print(f"👤 {stats['name']} the {stats['class']} (Level {stats['level']})")
        print(f"❤️  Health: {stats['health']}")
        print(f"⭐ Experience: {stats['experience']} XP")
        print(f"💰 Gold: {stats['gold']} coins")
        print(f"📍 Location: {stats['location']}")
        return stats
    
    elif action == "modify":
        original_value = player[stat]
        
        if stat == "health":
            player[stat] = max(0, min(player["max_health"], player[stat] + amount))
            if amount > 0:
                print(f"💚 Healed {amount} health! ({original_value} → {player[stat]})")
            else:
                print(f"💔 Took {abs(amount)} damage! ({original_value} → {player[stat]})")
        
        elif stat == "experience":
            player[stat] += amount
            print(f"⭐ Gained {amount} experience! ({original_value} → {player[stat]} XP)")
            
            # Check for level up
            xp_needed = player["level"] * 100
            if player[stat] >= xp_needed:
                return level_up_player()
        
        elif stat == "gold":
            player[stat] = max(0, player[stat] + amount)
            if amount > 0:
                print(f"💰 Found {amount} gold! ({original_value} → {player[stat]} coins)")
            else:
                print(f"💸 Spent {abs(amount)} gold! ({original_value} → {player[stat]} coins)")
        
        return player[stat]
    
    elif action == "level_up":
        return level_up_player()

def level_up_player():
    """Handle player level progression."""
    global GAME_STATE
    player = GAME_STATE["player"]
    
    player["level"] += 1
    health_increase = 20
    player["max_health"] += health_increase
    player["health"] = player["max_health"]  # Full heal on level up
    
    level_up_data = {
        "new_level": player["level"],
        "health_bonus": health_increase,
        "new_max_health": player["max_health"],
        "abilities_unlocked": []
    }
    
    # Add class-specific bonuses
    if player["class"] == "Warrior":
        level_up_data["abilities_unlocked"].append("🛡️ Improved Defense")
    elif player["class"] == "Mage":
        level_up_data["abilities_unlocked"].append("🔮 New Spell Learned")
    elif player["class"] == "Rogue":
        level_up_data["abilities_unlocked"].append("🗡️ Sneak Attack Improved")
    
    print(f"🎉 LEVEL UP! You are now level {player['level']}!")
    print(f"❤️  Max Health increased by {health_increase}! ({player['max_health']} total)")
    print(f"✨ {', '.join(level_up_data['abilities_unlocked'])}")
    
    return level_up_data

def manage_inventory(action, item=None, quantity=1):
    """
    Manage player inventory (add, remove, list items).
    """
    global GAME_STATE
    inventory = GAME_STATE["player"]["inventory"]
    
    if action == "list":
        print(f"🎒 INVENTORY ({len(inventory)} items):")
        if not inventory:
            print("   📦 Empty - time to find some loot!")
        else:
            for i, item in enumerate(inventory, 1):
                print(f"   {i}. {item}")
        return inventory
    
    elif action == "add":
        for _ in range(quantity):
            inventory.append(item)
        print(f"📦 Added {quantity}x {item} to inventory!")
        GAME_STATE["session_stats"]["treasures_found"] += 1
        return f"Added {item}"
    
    elif action == "remove":
        if item in inventory:
            inventory.remove(item)
            print(f"✅ Used {item} from inventory!")
            return f"Used {item}"
        else:
            print(f"❌ You don't have {item} in your inventory!")
            return f"Don't have {item}"
    
    elif action == "use":
        if item in inventory:
            inventory.remove(item)
            
            # Handle item effects
            if "Health Potion" in item:
                heal_amount = 30
                manage_player_stats("modify", "health", heal_amount)
                return f"Used {item} - healed {heal_amount} health!"
            elif "Mana Potion" in item:
                print("💙 Mana restored! Ready to cast spells!")
                return f"Used {item} - mana restored!"
            else:
                print(f"✨ Used {item} - effects applied!")
                return f"Used {item}"
        else:
            return f"You don't have {item}!"

def combat_system(enemy_name, enemy_health=30, enemy_attack=8):
    """
    Handle turn-based combat encounters.
    """
    global GAME_STATE
    
    print(f"⚔️  COMBAT ENCOUNTER!")
    print(f"🐉 A wild {enemy_name} appears!")
    print(f"❤️  Enemy Health: {enemy_health}")
    print(f"🗡️ Enemy Attack: {enemy_attack}")
    
    player = GAME_STATE["player"]
    current_enemy_health = enemy_health
    round_num = 1
    
    combat_log = {
        "enemy": enemy_name,
        "rounds": [],
        "victory": False,
        "player_health_start": player["health"],
        "player_health_end": 0
    }
    
    while current_enemy_health > 0 and player["health"] > 0:
        print(f"\n🔄 ROUND {round_num}")
        print(f"👤 Your Health: {player['health']}/{player['max_health']}")
        print(f"🐉 {enemy_name} Health: {current_enemy_health}/{enemy_health}")
        
        # Player attack
        player_roll = roll_dice(1, 20, modifier=2, purpose="player attack")
        player_damage = max(1, player_roll["total"] - 10)  # Minimum 1 damage
        current_enemy_health -= player_damage
        
        round_data = {
            "round": round_num,
            "player_roll": player_roll["total"],
            "player_damage": player_damage,
            "enemy_damage": 0
        }
        
        print(f"⚔️  You deal {player_damage} damage to {enemy_name}!")
        
        if current_enemy_health <= 0:
            print(f"🎉 Victory! {enemy_name} is defeated!")
            combat_log["victory"] = True
            break
        
        # Enemy attack
        enemy_roll = roll_dice(1, 20, purpose="enemy attack")
        enemy_damage_dealt = max(1, enemy_roll["total"] - 8)  # Player has some defense
        player["health"] -= enemy_damage_dealt
        round_data["enemy_damage"] = enemy_damage_dealt
        
        print(f"💥 {enemy_name} deals {enemy_damage_dealt} damage to you!")
        
        combat_log["rounds"].append(round_data)
        round_num += 1
    
    combat_log["player_health_end"] = player["health"]
    
    if player["health"] <= 0:
        print("💀 Defeat! You have fallen in battle!")
        print("🏥 Respawning at the village with 1 health...")
        player["health"] = 1
        player["location"] = "Village"
        return combat_log
    
    # Victory rewards
    xp_reward = enemy_health + 10
    gold_reward = random.randint(10, 30)
    
    manage_player_stats("modify", "experience", xp_reward)
    manage_player_stats("modify", "gold", gold_reward)
    GAME_STATE["session_stats"]["battles_won"] += 1
    
    # Random treasure chance
    if random.randint(1, 100) <= 30:  # 30% chance
        treasures = ["Magic Ring", "Silver Dagger", "Enchanted Amulet", "Health Potion", "Mana Potion"]
        treasure = random.choice(treasures)
        manage_inventory("add", treasure)
    
    return combat_log

def generate_encounter(location="wilderness"):
    """
    Generate random encounters based on location.
    """
    encounters = {
        "wilderness": [
            {"type": "combat", "enemy": "Goblin Scout", "health": 20, "attack": 6},
            {"type": "combat", "enemy": "Wild Wolf", "health": 25, "attack": 8},
            {"type": "treasure", "item": "Ancient Coin", "gold": 25},
            {"type": "treasure", "item": "Health Potion", "gold": 0},
            {"type": "skill", "challenge": "Navigate through thorns", "difficulty": 12}
        ],
        "dungeon": [
            {"type": "combat", "enemy": "Skeleton Warrior", "health": 35, "attack": 10},
            {"type": "combat", "enemy": "Cave Spider", "health": 15, "attack": 12},
            {"type": "treasure", "item": "Magic Sword", "gold": 50},
            {"type": "skill", "challenge": "Pick ancient lock", "difficulty": 15}
        ],
        "village": [
            {"type": "treasure", "item": "Village Gift", "gold": 10},
            {"type": "skill", "challenge": "Persuade merchant for discount", "difficulty": 10}
        ]
    }
    
    location_encounters = encounters.get(location, encounters["wilderness"])
    encounter = random.choice(location_encounters)
    
    print(f"🎯 Random encounter in {location}...")
    
    if encounter["type"] == "combat":
        print(f"⚔️  You encounter a {encounter['enemy']}!")
        return combat_system(encounter["enemy"], encounter["health"], encounter["attack"])
    
    elif encounter["type"] == "treasure":
        print(f"💎 You discover: {encounter['item']}!")
        manage_inventory("add", encounter["item"])
        if encounter["gold"] > 0:
            manage_player_stats("modify", "gold", encounter["gold"])
        return {"type": "treasure", "item": encounter["item"], "gold": encounter["gold"]}
    
    elif encounter["type"] == "skill":
        challenge = encounter["challenge"]
        difficulty = encounter["difficulty"]
        print(f"🎯 Skill Challenge: {challenge}")
        print(f"📊 Difficulty: {difficulty}")
        
        skill_roll = roll_dice(1, 20, modifier=3, purpose=f"skill check: {challenge}")
        success = skill_roll["total"] >= difficulty
        
        GAME_STATE["session_stats"]["skills_used"] += 1
        
        result = {"type": "skill", "challenge": challenge, "success": success, "roll": skill_roll["total"]}
        
        if success:
            print("🎉 Success! Your skills prove useful!")
            reward = random.choice(["Health Potion", "Gold Coins", "Experience"])
            if reward == "Gold Coins":
                manage_player_stats("modify", "gold", 20)
            elif reward == "Experience":
                manage_player_stats("modify", "experience", 25)
            else:
                manage_inventory("add", reward)
        else:
            print("😅 Not quite successful, but you learn from the experience!")
            manage_player_stats("modify", "experience", 5)
        
        return result

def save_game_state():
    """Save current game state."""
    try:
        save_data = {
            "player": GAME_STATE["player"],
            "session_stats": GAME_STATE["session_stats"],
            "saved_at": datetime.now().isoformat()
        }
        
        with open("dungeon_save.json", "w") as f:
            json.dump(save_data, f, indent=2)
        
        print("💾 Game saved successfully!")
        return "Game saved"
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return f"Save failed: {e}"

def load_game_state():
    """Load saved game state."""
    global GAME_STATE
    try:
        with open("dungeon_save.json", "r") as f:
            save_data = json.load(f)
        
        GAME_STATE["player"] = save_data["player"]
        GAME_STATE["session_stats"] = save_data["session_stats"]
        
        print("📂 Game loaded successfully!")
        print(f"🎮 Welcome back, {GAME_STATE['player']['name']}!")
        return "Game loaded"
    except FileNotFoundError:
        print("💾 No save file found. Starting fresh adventure!")
        return "No save file"
    except Exception as e:
        print(f"❌ Load failed: {e}")
        return f"Load failed: {e}"

# Define dungeon master tools for AI
DUNGEON_MASTER_TOOLS = [
    {
        "name": "roll_dice",
        "description": "Roll dice for combat, skill checks, and random events with dramatic flair",
        "parameters": {
            "type": "object",
            "properties": {
                "num_dice": {"type": "integer", "description": "Number of dice to roll", "default": 1},
                "sides": {"type": "integer", "description": "Number of sides on each die", "default": 20},
                "modifier": {"type": "integer", "description": "Bonus/penalty to add to roll", "default": 0},
                "purpose": {"type": "string", "description": "What the roll is for (e.g., 'attack roll', 'skill check')"}
            },
            "required": ["purpose"]
        }
    },
    {
        "name": "manage_player_stats",
        "description": "Manage player statistics including health, experience, gold, and level progression",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["get_stats", "modify", "level_up"], "description": "Action to perform"},
                "stat": {"type": "string", "enum": ["health", "experience", "gold", "level"], "description": "Which stat to modify"},
                "amount": {"type": "integer", "description": "Amount to add/subtract"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "manage_inventory",
        "description": "Manage player inventory including adding items, using potions, and listing equipment",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["list", "add", "remove", "use"], "description": "Inventory action"},
                "item": {"type": "string", "description": "Item name"},
                "quantity": {"type": "integer", "description": "How many items", "default": 1}
            },
            "required": ["action"]
        }
    },
    {
        "name": "combat_system",
        "description": "Initiate turn-based combat with enemies including dice rolls and damage calculation",
        "parameters": {
            "type": "object",
            "properties": {
                "enemy_name": {"type": "string", "description": "Name of the enemy to fight"},
                "enemy_health": {"type": "integer", "description": "Enemy's health points", "default": 30},
                "enemy_attack": {"type": "integer", "description": "Enemy's attack power", "default": 8}
            },
            "required": ["enemy_name"]
        }
    },
    {
        "name": "generate_encounter",
        "description": "Generate random encounters including combat, treasure, and skill challenges",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "enum": ["wilderness", "dungeon", "village"], "description": "Current location type"}
            },
            "required": ["location"]
        }
    },
    {
        "name": "save_game_state",
        "description": "Save the current game progress to continue later",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "load_game_state", 
        "description": "Load previously saved game progress",
        "parameters": {"type": "object", "properties": {}}
    }
]

def play_with_ai_dungeon_master(player_action):
    """
    Send player action to AI Dungeon Master for processing.
    """
    print(f"🎭 You: {player_action}")
    print("🤖 AI Dungeon Master is processing your action...")
    
    # Get API key
    api_key = os.getenv('INCREDIBLE_API_KEY')
    if not api_key:
        print("❌ Missing INCREDIBLE_API_KEY!")
        return
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # System prompt for the AI Dungeon Master
    system_prompt = f"""You are an expert AI Dungeon Master running an interactive RPG adventure. You have access to comprehensive game mechanics through function calls.

Current Game State:
- Player: {GAME_STATE['player']['name']} the {GAME_STATE['player']['class']} (Level {GAME_STATE['player']['level']})
- Health: {GAME_STATE['player']['health']}/{GAME_STATE['player']['max_health']}
- Location: {GAME_STATE['player']['location']}
- Experience: {GAME_STATE['player']['experience']} XP
- Gold: {GAME_STATE['player']['gold']} coins

Your role:
- Narrate the adventure with vivid, engaging descriptions
- Use dice rolls for all uncertain outcomes
- Manage combat, exploration, and character progression
- Present meaningful choices to the player
- Create an immersive fantasy world experience
- Balance challenge and fun

Always use appropriate function calls for:
- Dice rolling (combat, skill checks, random events)
- Health/stats management (damage, healing, experience)
- Inventory operations (finding items, using potions)
- Combat encounters (when fighting enemies)
- Random encounters (exploration events)

Make the story interactive and engaging! Ask the player what they want to do next."""
    
    # Prepare the message
    messages = [{"role": "user", "content": player_action}]
    
    initial_data = {
        "model": "small-1",
        "stream": False,
        "system": system_prompt,
        "messages": messages,
        "functions": DUNGEON_MASTER_TOOLS
    }
    
    try:
        # Step 1: Send initial request
        response = requests.post('https://api.incredible.one/v1/chat-completion',
                               headers=headers, json=initial_data)
        response.raise_for_status()
        
        result = response.json()
        response_items = result['result']['response']
        
        # Look for function calls
        function_call_item = None
        assistant_message = None
        
        for item in response_items:
            if item.get('type') == 'function_call':
                function_call_item = item
            elif item.get('role') == 'assistant':
                assistant_message = item
        
        if function_call_item:
            print("🎲 AI Dungeon Master is using game mechanics...")
            
            function_call_id = function_call_item['function_call_id']
            function_calls = function_call_item['function_calls']
            
            # Execute the functions
            function_results = []
            for func_call in function_calls:
                function_name = func_call['name']
                function_input = func_call['input']
                
                print(f"⚡ DM Action: {function_name}")
                
                # Call the appropriate function
                if function_name == "roll_dice":
                    result = roll_dice(**function_input)
                elif function_name == "manage_player_stats":
                    result = manage_player_stats(**function_input)
                elif function_name == "manage_inventory":
                    result = manage_inventory(**function_input)
                elif function_name == "combat_system":
                    result = combat_system(**function_input)
                elif function_name == "generate_encounter":
                    result = generate_encounter(**function_input)
                elif function_name == "save_game_state":
                    result = save_game_state()
                elif function_name == "load_game_state":
                    result = load_game_state()
                else:
                    result = f"Unknown function: {function_name}"
                
                function_results.append(result)
            
            # Prepare messages for second API call
            messages_history = [{"role": "user", "content": player_action}]
            
            if assistant_message:
                messages_history.append(assistant_message)
            
            messages_history.extend([
                function_call_item,
                {
                    "type": "function_call_result",
                    "function_call_id": function_call_id,
                    "function_call_results": function_results
                }
            ])
            
            # Step 2: Get AI's narrative response
            print("📖 AI Dungeon Master narrating the results...")
            
            final_data = {
                "model": "small-1",
                "stream": False,
                "system": system_prompt,
                "messages": messages_history,
                "functions": DUNGEON_MASTER_TOOLS
            }
            
            final_response = requests.post('https://api.incredible.one/v1/chat-completion',
                                         headers=headers, json=final_data)
            final_response.raise_for_status()
            
            final_result = final_response.json()
            final_items = final_result['result']['response']
            
            # Extract the AI's story narration
            for item in final_items:
                if item.get('role') == 'assistant':
                    dm_response = item['content']
                    print("\n" + "="*60)
                    print("🎭 DUNGEON MASTER")
                    print("="*60)
                    print(dm_response)
                    print("="*60)
                    return dm_response
        
        # If no function calls, return the initial response
        elif assistant_message:
            dm_response = assistant_message['content']
            print("\n" + "="*60)
            print("🎭 DUNGEON MASTER")
            print("="*60)
            print(dm_response)
            print("="*60)
            return dm_response
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def start_adventure():
    """
    Initialize the game and start the adventure.
    """
    print("🏰 WELCOME TO THE AI DUNGEON MASTER!")
    print("="*50)
    
    # Check if there's a saved game
    print("💾 Checking for saved games...")
    load_result = load_game_state()
    
    if "No save file" in load_result:
        print("\n🎯 NEW ADVENTURE!")
        print("Let's create your character:")
        
        # Character creation
        name = input("⚔️  Enter your character's name: ").strip()
        if not name:
            name = "Adventurer"
        
        print("\n🎭 Choose your class:")
        print("1. ⚔️  Warrior (Strong in combat)")
        print("2. 🔮 Mage (Magical abilities)")  
        print("3. 🗡️ Rogue (Stealth and agility)")
        
        class_choice = input("Enter 1, 2, or 3: ").strip()
        class_map = {"1": "Warrior", "2": "Mage", "3": "Rogue"}
        character_class = class_map.get(class_choice, "Warrior")
        
        # Update game state
        GAME_STATE["player"]["name"] = name
        GAME_STATE["player"]["class"] = character_class
        
        print(f"\n🎉 Welcome, {name} the {character_class}!")
        print("Your adventure begins...")
        
        # Start the adventure
        opening_action = f"I am {name} the {character_class}. I just arrived at a mysterious village tavern at sunset. What do I see and what can I do?"
    else:
        print(f"\n🎮 Welcome back to your adventure!")
        opening_action = "I want to continue my adventure. Remind me where I am and what's happening."
    
    # Start the interactive game loop
    current_action = opening_action
    turn_count = 1
    
    print("\n" + "🎲" * 20)
    print("INTERACTIVE RPG ADVENTURE BEGINS!")
    print("🎲" * 20)
    print("\n💡 Type your actions like:")
    print("   • 'look around'")
    print("   • 'attack the goblin'") 
    print("   • 'check my inventory'")
    print("   • 'drink health potion'")
    print("   • 'save game'")
    print("   • 'quit' to exit")
    
    while True:
        print(f"\n🎯 TURN {turn_count}")
        print("-" * 30)
        
        # Send action to AI Dungeon Master
        ai_response = play_with_ai_dungeon_master(current_action)
        
        if not ai_response:
            break
            
        # Get player's next action
        print(f"\n🎮 What do you want to do next?")
        next_action = input("👤 Your action: ").strip()
        
        if not next_action:
            next_action = "I wait and observe my surroundings."
        elif next_action.lower() in ['quit', 'exit']:
            print("🌅 Thanks for playing! Your adventure will be saved.")
            save_game_state()
            break
        
        current_action = next_action
        turn_count += 1
        
        # Show session stats every 5 turns
        if turn_count % 5 == 0:
            stats = GAME_STATE["session_stats"]
            print(f"\n📊 SESSION STATS:")
            print(f"🎲 Dice Rolled: {stats['dice_rolled']}")
            print(f"⚔️  Battles Won: {stats['battles_won']}")
            print(f"💎 Treasures Found: {stats['treasures_found']}")
            print(f"🎯 Skills Used: {stats['skills_used']}")

def demo_game_mechanics():
    """
    Demonstrate the game mechanics without AI interaction.
    """
    print("🎮 GAME MECHANICS DEMO")
    print("=" * 30)
    
    # Set up a demo character
    GAME_STATE["player"]["name"] = "Demo Hero"
    GAME_STATE["player"]["class"] = "Warrior"
    
    print("1. 📊 Character Stats:")
    manage_player_stats("get_stats")
    
    print("\n2. 🎲 Dice Rolling:")
    roll_dice(1, 20, 5, "demo attack")
    
    print("\n3. 🎒 Inventory Management:")
    manage_inventory("list")
    manage_inventory("add", "Magic Sword")
    manage_inventory("use", "Health Potion")
    
    print("\n4. ⚔️  Combat System:")
    combat_system("Training Dummy", 20, 5)
    
    print("\n5. 🎯 Random Encounter:")
    generate_encounter("wilderness")
    
    print("\n6. 💾 Save System:")
    save_game_state()

if __name__ == "__main__":
    print("🐉 AI DUNGEON MASTER - Interactive RPG Adventure")
    print("=" * 55)
    print("🎮 The most engaging way to learn function calling!")
    print("🎲 Experience AI storytelling with real game mechanics!")
    
    choice = input("\n🎯 Choose your experience:\n1. 🎮 Play Interactive Adventure\n2. 🔧 Demo Game Mechanics\n\nEnter 1 or 2: ").strip()
    
    if choice == "2":
        demo_game_mechanics()
    else:
        start_adventure()
    
    print("\n🎉 Thanks for playing the AI Dungeon Master!")
    print("💡 You just experienced function calling in the most fun way possible!")
    print("🚀 Now imagine using these concepts for:")
    print("   • Interactive customer service bots")
    print("   • Educational gamification systems")  
    print("   • Dynamic content generation")
    print("   • Personalized user experiences")
    print("\n⚡ Function calling + AI creativity = Endless possibilities! ✨")
