from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import time

app = FastAPI(
    title="Co-op Library Classroom Test API",
    description="Live target API for Module 1: Consuming APIs",
    version="1.2.0"
)

# --- Configuration ---
AUTH_ENABLED = True
VALID_TOKEN = "coop-learner-2026"
RATE_LIMIT_WINDOW = 10
MAX_REQUESTS = 5

# --- Persistence ---
templates = Jinja2Templates(directory="templates")
tasks_db = [
    # --- Fiction: English & American ---
    {"id": 1,  "title": "The Bone People",                         "description": "Keri Hulme",                          "completed": True,  "isbn": "978-0-14-011916-2", "barcode": "9780140119162", "dewey_decimal": "823",     "retail_price": 28.99, "secondhand_price": 8.00},
    {"id": 2,  "title": "The Handmaid's Tale",                     "description": "Margaret Atwood",                     "completed": False, "isbn": "978-0-385-49081-8", "barcode": "9780385490818", "dewey_decimal": "813",     "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 3,  "title": "Piranesi",                                "description": "Susanna Clarke",                      "completed": True,  "isbn": "978-1-52-662242-6", "barcode": "9781526622426", "dewey_decimal": "823",     "retail_price": 26.99, "secondhand_price": 9.00},
    {"id": 4,  "title": "The Midnight Library",                    "description": "Matt Haig",                           "completed": False, "isbn": "978-0-52-555947-4", "barcode": "9780525559474", "dewey_decimal": "823",     "retail_price": 24.99, "secondhand_price": 8.00},
    {"id": 5,  "title": "Circe",                                   "description": "Madeline Miller",                     "completed": True,  "isbn": "978-0-31-655634-7", "barcode": "9780316556347", "dewey_decimal": "813",     "retail_price": 27.99, "secondhand_price": 9.50},
    {"id": 6,  "title": "Mexican Gothic",                          "description": "Silvia Moreno-Garcia",                "completed": False, "isbn": "978-0-52-562069-5", "barcode": "9780525620695", "dewey_decimal": "863",     "retail_price": 26.99, "secondhand_price": 8.50},
    {"id": 7,  "title": "The Thursday Murder Club",                "description": "Richard Osman",                       "completed": True,  "isbn": "978-0-24-198538-7", "barcode": "9780241985387", "dewey_decimal": "823",     "retail_price": 24.99, "secondhand_price": 7.00},
    {"id": 8,  "title": "Lessons in Chemistry",                    "description": "Bonnie Garmus",                       "completed": False, "isbn": "978-0-38-553833-0", "barcode": "9780385538330", "dewey_decimal": "813",     "retail_price": 29.99, "secondhand_price": 10.00},
    {"id": 9,  "title": "Good Omens",                              "description": "Neil Gaiman & Terry Pratchett",       "completed": True,  "isbn": "978-0-06-085541-8", "barcode": "9780060855418", "dewey_decimal": "823",     "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 10, "title": "The Hitchhiker's Guide to the Galaxy",    "description": "Douglas Adams",                       "completed": False, "isbn": "978-0-34-539848-5", "barcode": "9780345398482", "dewey_decimal": "823",     "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 11, "title": "Where the Crawdads Sing",                 "description": "Delia Owens",                         "completed": True,  "isbn": "978-0-73-522076-9", "barcode": "9780735220768", "dewey_decimal": "813",     "retail_price": 27.99, "secondhand_price": 9.00},
    {"id": 12, "title": "Eleanor Oliphant is Completely Fine",     "description": "Gail Honeyman",                       "completed": False, "isbn": "978-0-00-821533-5", "barcode": "9780008215330", "dewey_decimal": "823",     "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 13, "title": "The Tattooist of Auschwitz",              "description": "Heather Morris",                      "completed": True,  "isbn": "978-1-52-661374-5", "barcode": "9781526613745", "dewey_decimal": "823",     "retail_price": 26.99, "secondhand_price": 8.50},
    {"id": 14, "title": "The Curious Incident of the Dog",         "description": "Mark Haddon",                         "completed": False, "isbn": "978-0-09-945025-5", "barcode": "9780099450253", "dewey_decimal": "823",     "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 15, "title": "I Know Why the Caged Bird Sings",         "description": "Maya Angelou",                        "completed": True,  "isbn": "978-0-34-531143-4", "barcode": "9780345311436", "dewey_decimal": "813",     "retail_price": 22.99, "secondhand_price": 6.50},
    # --- Fiction: World Literature ---
    {"id": 16, "title": "One Hundred Years of Solitude",           "description": "Gabriel García Márquez",              "completed": False, "isbn": "978-0-06-011490-7", "barcode": "9780060114909", "dewey_decimal": "863",     "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 17, "title": "The Alchemist",                           "description": "Paulo Coelho",                        "completed": True,  "isbn": "978-0-06-231500-4", "barcode": "9780062315007", "dewey_decimal": "869",     "retail_price": 22.99, "secondhand_price": 6.00},
    {"id": 18, "title": "The Little Prince",                       "description": "Antoine de Saint-Exupéry",            "completed": False, "isbn": "978-0-15-601219-5", "barcode": "9780156012195", "dewey_decimal": "843",     "retail_price": 19.99, "secondhand_price": 5.50},
    {"id": 19, "title": "Crime and Punishment",                    "description": "Fyodor Dostoevsky",                   "completed": True,  "isbn": "978-0-14-044913-7", "barcode": "9780140449136", "dewey_decimal": "891.73",  "retail_price": 19.99, "secondhand_price": 5.50},
    {"id": 20, "title": "Norwegian Wood",                          "description": "Haruki Murakami",                     "completed": False, "isbn": "978-0-37-571853-0", "barcode": "9780375718533", "dewey_decimal": "895.63",  "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 21, "title": "Kafka on the Shore",                      "description": "Haruki Murakami",                     "completed": True,  "isbn": "978-1-40-000951-0", "barcode": "9781400009510", "dewey_decimal": "895.63",  "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 22, "title": "The Shadow of the Wind",                  "description": "Carlos Ruiz Zafón",                   "completed": False, "isbn": "978-0-14-303490-5", "barcode": "9780143034902", "dewey_decimal": "863",     "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 23, "title": "Sophie's World",                          "description": "Jostein Gaarder",                     "completed": True,  "isbn": "978-0-37-470521-5", "barcode": "9780374705213", "dewey_decimal": "839.82",  "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 24, "title": "Anxious People",                          "description": "Fredrik Backman",                     "completed": False, "isbn": "978-1-50-118371-2", "barcode": "9781501183713", "dewey_decimal": "839.73",  "retail_price": 27.99, "secondhand_price": 8.50},
    {"id": 25, "title": "The Name of the Rose",                    "description": "Umberto Eco",                         "completed": True,  "isbn": "978-0-15-144647-6", "barcode": "9780151446472", "dewey_decimal": "853",     "retail_price": 22.99, "secondhand_price": 7.00},
    # --- Science & Nature ---
    {"id": 26, "title": "A Brief History of Time",                 "description": "Stephen Hawking",                     "completed": False, "isbn": "978-0-55-305703-9", "barcode": "9780553057034", "dewey_decimal": "523.1",   "retail_price": 24.99, "secondhand_price": 6.00},
    {"id": 27, "title": "A Short History of Nearly Everything",    "description": "Bill Bryson",                         "completed": True,  "isbn": "978-0-76-790818-4", "barcode": "9780767908184", "dewey_decimal": "500",     "retail_price": 29.99, "secondhand_price": 9.00},
    {"id": 28, "title": "The Selfish Gene",                        "description": "Richard Dawkins",                     "completed": False, "isbn": "978-0-19-286092-7", "barcode": "9780192860927", "dewey_decimal": "576.5",   "retail_price": 24.99, "secondhand_price": 7.00},
    {"id": 29, "title": "The Hidden Life of Trees",                "description": "Peter Wohlleben",                     "completed": True,  "isbn": "978-1-77-164115-7", "barcode": "9781771641159", "dewey_decimal": "582.16",  "retail_price": 29.99, "secondhand_price": 9.00},
    {"id": 30, "title": "The Sixth Extinction",                    "description": "Elizabeth Kolbert",                   "completed": False, "isbn": "978-0-80-508841-6", "barcode": "9780805088410", "dewey_decimal": "576.8",   "retail_price": 29.99, "secondhand_price": 9.00},
    {"id": 31, "title": "The Disappearing Spoon",                  "description": "Sam Kean",                            "completed": True,  "isbn": "978-0-31-609536-6", "barcode": "9780316095365", "dewey_decimal": "546",     "retail_price": 26.99, "secondhand_price": 8.00},
    {"id": 32, "title": "The Gene: An Intimate History",           "description": "Siddhartha Mukherjee",                "completed": False, "isbn": "978-1-47-670887-3", "barcode": "9781476708874", "dewey_decimal": "576.5",   "retail_price": 39.99, "secondhand_price": 14.00},
    {"id": 33, "title": "The Double Helix",                        "description": "James D. Watson",                     "completed": True,  "isbn": "978-0-74-326254-6", "barcode": "9780743262545", "dewey_decimal": "572.8",   "retail_price": 22.99, "secondhand_price": 7.00},
    {"id": 34, "title": "Surely You're Joking, Mr. Feynman!",     "description": "Richard P. Feynman",                   "completed": False, "isbn": "978-0-39-331709-0", "barcode": "9780393317091", "dewey_decimal": "530",     "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 35, "title": "Longitude",                               "description": "Dava Sobel",                          "completed": True,  "isbn": "978-0-14-258401-4", "barcode": "9780142584019", "dewey_decimal": "526",     "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 36, "title": "Fermat's Enigma",                         "description": "Simon Singh",                         "completed": False, "isbn": "978-0-38-549362-8", "barcode": "9780385493628", "dewey_decimal": "512.7",   "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 37, "title": "How to Lie with Statistics",              "description": "Darrell Huff",                        "completed": True,  "isbn": "978-0-39-331072-5", "barcode": "9780393310726", "dewey_decimal": "519.5",   "retail_price": 18.99, "secondhand_price": 5.50},
    {"id": 38, "title": "The Body: A Guide for Occupants",         "description": "Bill Bryson",                         "completed": False, "isbn": "978-0-38-554495-9", "barcode": "9780385544955", "dewey_decimal": "612",     "retail_price": 34.99, "secondhand_price": 12.00},
    {"id": 39, "title": "Why We Sleep",                            "description": "Matthew Walker",                      "completed": True,  "isbn": "978-1-50-114798-2", "barcode": "9781501147982", "dewey_decimal": "612.8",   "retail_price": 32.99, "secondhand_price": 11.00},
    {"id": 40, "title": "The Emperor of All Maladies",             "description": "Siddhartha Mukherjee",                "completed": False, "isbn": "978-1-43-915199-0", "barcode": "9781439151990", "dewey_decimal": "616.99",  "retail_price": 34.99, "secondhand_price": 12.00},
    # --- Technology & Computing ---
    {"id": 41, "title": "Clean Code",                              "description": "Robert C. Martin",                    "completed": True,  "isbn": "978-0-13-235088-4", "barcode": "9780132350884", "dewey_decimal": "005.13",  "retail_price": 59.99, "secondhand_price": 22.00},
    {"id": 42, "title": "The Pragmatic Programmer",                "description": "Andrew Hunt & David Thomas",           "completed": False, "isbn": "978-0-13-595705-9", "barcode": "9780135957059", "dewey_decimal": "004",     "retail_price": 64.99, "secondhand_price": 25.00},
    {"id": 43, "title": "The Innovators",                          "description": "Walter Isaacson",                     "completed": True,  "isbn": "978-1-47-677869-2", "barcode": "9781476778693", "dewey_decimal": "004",     "retail_price": 34.99, "secondhand_price": 12.00},
    {"id": 44, "title": "The Code Book",                           "description": "Simon Singh",                         "completed": False, "isbn": "978-0-38-549532-5", "barcode": "9780385495325", "dewey_decimal": "005.8",   "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 45, "title": "Thinking in Systems",                     "description": "Donella H. Meadows",                  "completed": True,  "isbn": "978-1-60-358055-7", "barcode": "9781603580557", "dewey_decimal": "003",     "retail_price": 34.99, "secondhand_price": 12.00},
    # --- Psychology & Behaviour ---
    {"id": 46, "title": "Thinking, Fast and Slow",                 "description": "Daniel Kahneman",                     "completed": False, "isbn": "978-0-37-453355-7", "barcode": "9780374533557", "dewey_decimal": "153.4",   "retail_price": 32.99, "secondhand_price": 11.00},
    {"id": 47, "title": "Atomic Habits",                           "description": "James Clear",                         "completed": True,  "isbn": "978-0-73-521129-2", "barcode": "9780735211292", "dewey_decimal": "158.1",   "retail_price": 34.99, "secondhand_price": 12.00},
    {"id": 48, "title": "The Power of Habit",                      "description": "Charles Duhigg",                      "completed": False, "isbn": "978-0-81-298160-5", "barcode": "9780812981605", "dewey_decimal": "153.3",   "retail_price": 29.99, "secondhand_price": 9.50},
    {"id": 49, "title": "Quiet",                                   "description": "Susan Cain",                          "completed": True,  "isbn": "978-0-30-740412-1", "barcode": "9780307404121", "dewey_decimal": "155.2",   "retail_price": 29.99, "secondhand_price": 9.50},
    {"id": 50, "title": "Grit",                                    "description": "Angela Duckworth",                    "completed": False, "isbn": "978-1-50-110989-8", "barcode": "9781501109898", "dewey_decimal": "153.1",   "retail_price": 29.99, "secondhand_price": 9.00},
    {"id": 51, "title": "Make It Stick",                           "description": "Brown, Roediger & McDaniel",           "completed": True,  "isbn": "978-0-67-472442-2", "barcode": "9780674724426", "dewey_decimal": "153.1",   "retail_price": 29.99, "secondhand_price": 9.00},
    {"id": 52, "title": "Predictably Irrational",                  "description": "Dan Ariely",                          "completed": False, "isbn": "978-0-06-135323-9", "barcode": "9780061353239", "dewey_decimal": "330.01",  "retail_price": 27.99, "secondhand_price": 8.50},
    {"id": 53, "title": "Never Split the Difference",              "description": "Chris Voss",                          "completed": True,  "isbn": "978-0-06-240780-1", "barcode": "9780062407801", "dewey_decimal": "158.5",   "retail_price": 32.99, "secondhand_price": 11.00},
    {"id": 54, "title": "Ikigai",                                  "description": "Héctor García & Francesc Miralles",   "completed": False, "isbn": "978-0-14-313206-3", "barcode": "9780143132066", "dewey_decimal": "152.4",   "retail_price": 27.99, "secondhand_price": 8.50},
    {"id": 55, "title": "Range",                                   "description": "David Epstein",                       "completed": True,  "isbn": "978-0-73-521784-3", "barcode": "9780735217844", "dewey_decimal": "153.9",   "retail_price": 32.99, "secondhand_price": 11.00},
    # --- Social Sciences & Economics ---
    {"id": 56, "title": "Freakonomics",                            "description": "Steven Levitt & Stephen Dubner",      "completed": False, "isbn": "978-0-06-073132-6", "barcode": "9780060731328", "dewey_decimal": "330",     "retail_price": 27.99, "secondhand_price": 8.00},
    {"id": 57, "title": "Outliers",                                "description": "Malcolm Gladwell",                    "completed": True,  "isbn": "978-0-31-601792-3", "barcode": "9780316017923", "dewey_decimal": "302",     "retail_price": 27.99, "secondhand_price": 8.50},
    {"id": 58, "title": "The Tipping Point",                       "description": "Malcolm Gladwell",                    "completed": False, "isbn": "978-0-31-634662-7", "barcode": "9780316346627", "dewey_decimal": "302",     "retail_price": 27.99, "secondhand_price": 8.00},
    {"id": 59, "title": "Capital in the Twenty-First Century",     "description": "Thomas Piketty",                      "completed": True,  "isbn": "978-0-67-443000-6", "barcode": "9780674430006", "dewey_decimal": "332.041", "retail_price": 49.99, "secondhand_price": 18.00},
    {"id": 60, "title": "Good to Great",                           "description": "Jim Collins",                         "completed": False, "isbn": "978-0-06-662099-2", "barcode": "9780066620992", "dewey_decimal": "658.4",   "retail_price": 34.99, "secondhand_price": 12.00},
    {"id": 61, "title": "Why Nations Fail",                        "description": "Daron Acemoglu & James A. Robinson",  "completed": True,  "isbn": "978-0-30-771922-5", "barcode": "9780307719225", "dewey_decimal": "338.9",   "retail_price": 34.99, "secondhand_price": 12.00},
    {"id": 62, "title": "Guns, Germs, and Steel",                  "description": "Jared Diamond",                       "completed": False, "isbn": "978-0-39-331755-7", "barcode": "9780393317558", "dewey_decimal": "303.4",   "retail_price": 29.99, "secondhand_price": 9.50},
    {"id": 63, "title": "This Changes Everything",                 "description": "Naomi Klein",                         "completed": True,  "isbn": "978-1-45-165196-4", "barcode": "9781451651966", "dewey_decimal": "363.7",   "retail_price": 29.99, "secondhand_price": 9.50},
    {"id": 64, "title": "Digital Minimalism",                      "description": "Cal Newport",                         "completed": False, "isbn": "978-0-52-554287-2", "barcode": "9780525542872", "dewey_decimal": "303.48",  "retail_price": 29.99, "secondhand_price": 9.50},
    {"id": 65, "title": "The New Jim Crow",                        "description": "Michelle Alexander",                  "completed": True,  "isbn": "978-1-59-558643-8", "barcode": "9781595586438", "dewey_decimal": "364.1",   "retail_price": 29.99, "secondhand_price": 9.50},
    {"id": 66, "title": "Between the World and Me",                "description": "Ta-Nehisi Coates",                    "completed": False, "isbn": "978-0-81-299543-5", "barcode": "9780812995435", "dewey_decimal": "305.896", "retail_price": 24.99, "secondhand_price": 7.50},
    # --- History & Geography ---
    {"id": 67, "title": "Sapiens",                                 "description": "Yuval Noah Harari",                   "completed": True,  "isbn": "978-0-06-231609-7", "barcode": "9780062316097", "dewey_decimal": "909",     "retail_price": 34.99, "secondhand_price": 12.00},
    {"id": 68, "title": "Homo Deus",                               "description": "Yuval Noah Harari",                   "completed": False, "isbn": "978-0-06-246431-4", "barcode": "9780062464316", "dewey_decimal": "909",     "retail_price": 34.99, "secondhand_price": 12.00},
    {"id": 69, "title": "The Silk Roads",                          "description": "Peter Frankopan",                     "completed": True,  "isbn": "978-1-10-190217-0", "barcode": "9781101902171", "dewey_decimal": "909",     "retail_price": 39.99, "secondhand_price": 14.00},
    {"id": 70, "title": "The Diary of a Young Girl",               "description": "Anne Frank",                          "completed": False, "isbn": "978-0-55-329698-9", "barcode": "9780553296983", "dewey_decimal": "940.5318", "retail_price": 18.99, "secondhand_price": 5.50},
    {"id": 71, "title": "A People's History of the United States", "description": "Howard Zinn",                         "completed": True,  "isbn": "978-0-06-052837-9", "barcode": "9780060528379", "dewey_decimal": "973",     "retail_price": 34.99, "secondhand_price": 12.00},
    {"id": 72, "title": "The Penguin History of New Zealand",      "description": "Michael King",                        "completed": False, "isbn": "978-0-14-301867-4", "barcode": "9780143018674", "dewey_decimal": "993",     "retail_price": 39.99, "secondhand_price": 15.00},
    {"id": 73, "title": "Into Thin Air",                           "description": "Jon Krakauer",                        "completed": True,  "isbn": "978-0-38-549478-6", "barcode": "9780385494786", "dewey_decimal": "796.52",  "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 74, "title": "The Map That Changed the World",          "description": "Simon Winchester",                    "completed": False, "isbn": "978-0-06-093137-8", "barcode": "9780060931377", "dewey_decimal": "551.7",   "retail_price": 27.99, "secondhand_price": 8.50},
    {"id": 75, "title": "The Signal and the Noise",                "description": "Nate Silver",                         "completed": True,  "isbn": "978-0-14-312508-9", "barcode": "9780143125082", "dewey_decimal": "519.5",   "retail_price": 29.99, "secondhand_price": 9.50},
    # --- Philosophy & Ethics ---
    {"id": 76, "title": "Justice",                                 "description": "Michael J. Sandel",                   "completed": False, "isbn": "978-0-37-453255-0", "barcode": "9780374532550", "dewey_decimal": "172",     "retail_price": 29.99, "secondhand_price": 9.00},
    {"id": 77, "title": "The Prince",                              "description": "Niccolò Machiavelli",                 "completed": True,  "isbn": "978-0-14-044915-1", "barcode": "9780140449150", "dewey_decimal": "320.1",   "retail_price": 14.99, "secondhand_price": 4.00},
    {"id": 78, "title": "The Art of War",                          "description": "Sun Tzu",                             "completed": False, "isbn": "978-1-59-030895-0", "barcode": "9781590308950", "dewey_decimal": "355.02",  "retail_price": 18.99, "secondhand_price": 5.00},
    {"id": 79, "title": "Meditations",                             "description": "Marcus Aurelius",                     "completed": True,  "isbn": "978-0-14-044140-7", "barcode": "9780140441406", "dewey_decimal": "188",     "retail_price": 14.99, "secondhand_price": 4.00},
    {"id": 80, "title": "The Checklist Manifesto",                 "description": "Atul Gawande",                        "completed": False, "isbn": "978-0-80-509174-8", "barcode": "9780805091748", "dewey_decimal": "610.69",  "retail_price": 27.99, "secondhand_price": 8.50},
    # --- Arts, Music & Architecture ---
    {"id": 81, "title": "Ways of Seeing",                          "description": "John Berger",                         "completed": True,  "isbn": "978-0-14-013515-5", "barcode": "9780140135152", "dewey_decimal": "701",     "retail_price": 24.99, "secondhand_price": 7.00},
    {"id": 82, "title": "The Architecture of Happiness",           "description": "Alain de Botton",                     "completed": False, "isbn": "978-0-37-542449-8", "barcode": "9780375424496", "dewey_decimal": "720.1",   "retail_price": 32.99, "secondhand_price": 11.00},
    {"id": 83, "title": "This Is Your Brain on Music",             "description": "Daniel J. Levitin",                   "completed": True,  "isbn": "978-0-45-228960-4", "barcode": "9780452289604", "dewey_decimal": "781",     "retail_price": 29.99, "secondhand_price": 9.50},
    {"id": 84, "title": "Born to Run",                             "description": "Christopher McDougall",               "completed": False, "isbn": "978-0-30-726630-7", "barcode": "9780307266309", "dewey_decimal": "796.42",  "retail_price": 27.99, "secondhand_price": 8.50},
    {"id": 85, "title": "Salt Fat Acid Heat",                      "description": "Samin Nosrat",                        "completed": True,  "isbn": "978-1-47-672773-7", "barcode": "9781476727738", "dewey_decimal": "641.5",   "retail_price": 49.99, "secondhand_price": 18.00},
    # --- Language & Writing ---
    {"id": 86, "title": "The Language Instinct",                   "description": "Steven Pinker",                       "completed": False, "isbn": "978-0-06-095833-1", "barcode": "9780060958336", "dewey_decimal": "410",     "retail_price": 29.99, "secondhand_price": 9.00},
    {"id": 87, "title": "Eats, Shoots & Leaves",                   "description": "Lynne Truss",                         "completed": True,  "isbn": "978-1-59-240087-4", "barcode": "9781592400874", "dewey_decimal": "428",     "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 88, "title": "The Sense of Style",                      "description": "Steven Pinker",                       "completed": False, "isbn": "978-0-67-772905-9", "barcode": "9780677229058", "dewey_decimal": "808",     "retail_price": 29.99, "secondhand_price": 9.50},
    # --- Memoir & Narrative Non-Fiction ---
    {"id": 89, "title": "Educated",                                "description": "Tara Westover",                       "completed": True,  "isbn": "978-0-39-959050-4", "barcode": "9780399590504", "dewey_decimal": "378",     "retail_price": 29.99, "secondhand_price": 10.00},
    {"id": 90, "title": "The Immortal Life of Henrietta Lacks",    "description": "Rebecca Skloot",                      "completed": False, "isbn": "978-1-40-003533-5", "barcode": "9781400035335", "dewey_decimal": "616.02",  "retail_price": 27.99, "secondhand_price": 8.50},
    {"id": 91, "title": "In Cold Blood",                           "description": "Truman Capote",                       "completed": True,  "isbn": "978-0-67-974558-5", "barcode": "9780679745587", "dewey_decimal": "364.15",  "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 92, "title": "Bad Science",                             "description": "Ben Goldacre",                        "completed": False, "isbn": "978-0-00-724019-7", "barcode": "9780007240197", "dewey_decimal": "500",     "retail_price": 22.99, "secondhand_price": 7.00},
    {"id": 93, "title": "Steve Jobs",                              "description": "Walter Isaacson",                     "completed": True,  "isbn": "978-1-45-168992-4", "barcode": "9781451689228", "dewey_decimal": "338.7",   "retail_price": 34.99, "secondhand_price": 11.00},
    # --- Folklore, Food & Sport ---
    {"id": 94, "title": "Grimm's Fairy Tales",                     "description": "Brothers Grimm",                      "completed": False, "isbn": "978-0-14-243718-6", "barcode": "9780142437186", "dewey_decimal": "398.2",   "retail_price": 22.99, "secondhand_price": 7.00},
    {"id": 95, "title": "The Omnivore's Dilemma",                  "description": "Michael Pollan",                      "completed": True,  "isbn": "978-0-14-303858-3", "barcode": "9780143038580", "dewey_decimal": "641.3",   "retail_price": 29.99, "secondhand_price": 9.00},
    # --- More Fiction ---
    {"id": 96, "title": "The Kite Runner",                         "description": "Khaled Hosseini",                     "completed": False, "isbn": "978-1-59-463193-9", "barcode": "9781594631931", "dewey_decimal": "813",     "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 97, "title": "The Rosie Project",                       "description": "Graeme Simsion",                      "completed": True,  "isbn": "978-1-47-360358-2", "barcode": "9781473603585", "dewey_decimal": "823",     "retail_price": 24.99, "secondhand_price": 7.50},
    {"id": 98, "title": "Deep Work",                               "description": "Cal Newport",                         "completed": False, "isbn": "978-1-45-554129-0", "barcode": "9781455541290", "dewey_decimal": "153.4",   "retail_price": 29.99, "secondhand_price": 9.50},
    {"id": 99, "title": "Zero: The Biography of a Dangerous Idea", "description": "Charles Seife",                       "completed": True,  "isbn": "978-0-14-029647-1", "barcode": "9780140296471", "dewey_decimal": "511.2",   "retail_price": 22.99, "secondhand_price": 6.50},
    {"id": 100,"title": "The Testaments",                          "description": "Margaret Atwood",                     "completed": False, "isbn": "978-0-38-554390-7", "barcode": "9780385543903", "dewey_decimal": "813",     "retail_price": 34.99, "secondhand_price": 12.00},
]
traffic_logs = []
request_tracker = {}


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    isbn: Optional[str] = None
    barcode: Optional[str] = None
    dewey_decimal: Optional[str] = None
    retail_price: Optional[float] = None
    secondhand_price: Optional[float] = None


# --- Internal Logic ---

def log_activity(request: Request, action: str, status: int, details: str):
    client_ip = request.client.host if request.client else "Unknown"
    log_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "ip": client_ip,
        "action": action,
        "status": status,
        "details": details
    }
    traffic_logs.insert(0, log_entry)
    if len(traffic_logs) > 30: traffic_logs.pop()


def check_security_and_rate(request: Request):
    client_ip = request.client.host if request.client else "Unknown"
    now = time.time()

    # 1. Rate Limiting
    if client_ip not in request_tracker: request_tracker[client_ip] = []
    request_tracker[client_ip] = [t for t in request_tracker[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(request_tracker[client_ip]) >= MAX_REQUESTS:
        log_activity(request, f"{request.method} {request.url.path}", 429, "Rate limit exceeded")
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Slow down!")
    request_tracker[client_ip].append(now)

    # 2. Authentication Toggle
    if AUTH_ENABLED:
        auth_header = request.headers.get("Authorization")
        if not auth_header or auth_header != f"Bearer {VALID_TOKEN}":
            log_activity(request, f"{request.method} {request.url.path}", 401, "Auth Failed")
            raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid token.")


# --- UI & Dashboard ---

@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
async def dashboard_root(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/v1/internal/state", tags=["Dashboard"])
async def get_internal_state():
    return {
        "db": tasks_db,
        "logs": traffic_logs,
        "auth_status": AUTH_ENABLED
    }


# --- Student Endpoints ---

@app.get("/v1/books", tags=["Student Endpoints"])
async def get_books(request: Request, page: int = 1, limit: int = 10):
    check_security_and_rate(request)
    total = len(tasks_db)
    start = (page - 1) * limit
    end = start + limit
    page_items = tasks_db[start:end]
    log_activity(request, "GET /v1/books", 200, f"Page {page}, Limit {limit}, Total {total}")
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),  # ceiling division
        "results": page_items
    }


@app.post("/v1/books", status_code=201, tags=["Student Endpoints"])
async def create_book(task: Task, request: Request):
    check_security_and_rate(request)
    if any(t["id"] == task.id for t in tasks_db):
        log_activity(request, "POST /v1/books", 400, f"Duplicate ID: {task.id}")
        raise HTTPException(status_code=400, detail="ID already exists.")

    new_item = task.model_dump()
    tasks_db.append(new_item)
    log_activity(request, "POST /v1/books", 201, f"Created: {task.title}")
    return new_item


@app.put("/v1/books/{book_id}", tags=["Student Endpoints"])
async def update_book(book_id: int, task: Task, request: Request):
    check_security_and_rate(request)
    for idx, item in enumerate(tasks_db):
        if item["id"] == book_id:
            tasks_db[idx] = task.model_dump()
            log_activity(request, f"PUT /v1/books/{book_id}", 200, "Updated item")
            return tasks_db[idx]
    raise HTTPException(status_code=404, detail="Book not found.")


@app.delete("/v1/books/{book_id}", tags=["Student Endpoints"])
async def delete_book(book_id: int, request: Request):
    check_security_and_rate(request)
    for idx, item in enumerate(tasks_db):
        if item["id"] == book_id:
            removed = tasks_db.pop(idx)
            log_activity(request, f"DELETE /v1/books/{book_id}", 200, f"Deleted: {removed['title']}")
            return {"detail": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found.")


# --- Admin Controls ---

@app.post("/admin/toggle-auth", tags=["Admin"])
async def toggle_auth(request: Request):
    global AUTH_ENABLED
    AUTH_ENABLED = not AUTH_ENABLED
    log_activity(request, "ADMIN", 200, f"Auth toggled to {AUTH_ENABLED}")
    return {"auth_enabled": AUTH_ENABLED}