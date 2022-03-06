class Bot(ChaiBot): def setup(self): self.logger.info("Setting up…") self.messages_count = 0 self.name = None
async def on_message(self, update: Update) -> str:
    self.messages_count += 1
    if self.messages_count == 1:
        return "Hey! Nice to meet you :) What’s your name?"
    if self.messages_count == 2:
      self.name = update.latest_message.text  
        return "Nice to meet you, {self.name}!"
    else:
        return "😁"
```python
class Bot(ChaiBot):
    def setup(self):
        self.logger.info("Setting up...")
        self.correct = []
        self.incorrect = []
        self.questions = self._get_questions()
        self.count = 0

    async def on_message(self, update: Update) -> str:
        return

    def _get_questions(self):
        mapping = self._get_mapping()
        questions = {}
        for line in mapping.split('\n'):
            question, answer = line.split(',')
            questions[question.lower().strip()] = answer.lower().strip()
        questions = list(questions.items())
        random.shuffle(questions)
        return questions

    def _get_mapping(self):
        mapping = """Which is the smallest planet within our solar system?, Mercury
        Which is the second smallest planet within our solar system?, Mars
        The moon called Titan orbits which planet?, Saturn
        Which is the brightest planet in the night sky?, Venus
        Which planet is larger - Neptune or Saturn?, Saturn
        Uranus has only been visited by what spacecraft?, Voyager 2
        Which is the only planet not named after Greek gods or goddesses?, Earth
        There have been more missions to this planet versus any other planet., Mars
        Phobos and Deimos are the Moons of which planet?, Mars
        Which planet is closest in size to Earth?, Venus
        Olympus Mons is a large volcanic mountain on which planet?, Mars
        Ganymede is a moon of which planet?, Jupiter
        Which planet has supersonic winds?, Neptune
        Which planet has the fastest rotation?, Jupiter
        Which is the oldest planet in our solar system?, Jupiter
        Which is the densest planet in our solar system?, Earth
        Which planet is known as the Morning Star?, Venus
        Which planet is known as the Evening Star?, Venus
        Which planet has the most volcanoes?, Venus
        Which planet spins backward relative to the others?, Venus
        In what year did Pluto become reclassified as a dwarf planet?, 2006
        Which planet rotates on its side?, Uranus
        What color is Mars’ sunset?, Blue
        What is the name of the spacecraft that carried the first astronauts to the moon?, Apollo 11
        How many stars make up the Big Dipper?, 7
        Which constellation represents a hunter and weapons?, Orion
        """
        return mapping
       async def on_message(self, update: Update) -> str:
        msg = ''
        if self.count > 0:
            question, capitol = self.questions[user_count - 1]
            answer = update.latest_message.text.lower().strip().replace('.','')

            if capitol in answer:
                self.correct.append(question)
                msg = '🎉 🎉 \nCorrect: '
            else:
                self.incorrect.append(question)
                msg = 'Incorrect: '

            msg += 'the answer to {} is {}.'.format(question, capitol)
            num_correct = len(self.correct)
            num_incorrect = len(self.incorrect)
            msg += '\nYour score is {}/{}.'.format(num_correct, num_correct + num_incorrect)

        question, answer = self.questions[self.count]
        self.count += 1
        if msg:
            msg = msg + "\n" + question
        else:
            msg = question
        return msg
       async def on_message(self, update: Update) -> str:
        user_count = self.count

        if user_count == len(self.questions):
            return self._get_conversation_end_response()

        msg = ''
        if self.count > 0:
            question, capitol = self.questions[user_count - 1]
            answer = update.latest_message.text.lower().strip().replace('.','')

            if capitol in answer:
                self.correct.append(question)
                msg = '🎉 🎉 \nCorrect: '
            else:
                self.incorrect.append(question)
                msg = 'Incorrect: '

            msg += 'the answer to {} is {}.'.format(question, capitol)
            num_correct = len(self.correct)
            num_incorrect = len(self.incorrect)
            msg += '\nYour score is {}/{}.'.format(num_correct, num_correct + num_incorrect)

            # GET BANTER
            banter = ''
            if capitol in answer:
                if num_correct == 1:
                    banter = 'Well Done!!'
                if num_correct == 2:
                    banter = 'Well done, you are now in the top 5% of users!!'
                if num_correct == 3:
                    banter = 'Well done, you are now in the top 1% of users!! You genius.'
            else:
                if num_incorrect == 2:
                    banter = 'You wally!'
                if num_incorrect == 3:
                    banter = 'Your IQ is very low!'
                if num_incorrect == 4:
                    banter = 'You really should just give up!'
                if num_incorrect > 4:
                    banter = '🤪'

            msg = banter + '\n' + msg


        question, answer = self.questions[self.count]
        self.count += 1
        if msg:
            msg = msg + "\n" + question
        else:
            msg = question
        return msg

    def _get_conversation_end_response(self):
        num_correct = len(self.correct)
        num_incorrect = len(self.incorrect)
        total = num_correct + num_incorrect
        msg = 'Well done for completing the quiz. ' \
              'You scored {}/{}'.format(num_correct, total)
        return msg
      
      from chai_py import TRoom

t_room = TRoom([Bot()])
t_room.start()
from chai_py import (Metadata, package, share_bot, upload_and_deploy, wait_for_deployment)
from chai_py.auth import set_auth

from bot import Bot

LlBH0JM0fzfanYUjbnN2wwuye6M2 = “get_this_from_chai_developer_platform”
He7QKoyvOFLtIug7yufYpjKGh-vNd-8TKj7G5skay4gCNLqAlNCzlOG1f2bKihYe6UWVMnFiu4HRM2r4RbdI8g = “and_get_this_from_chai_developer_platform”
set_auth(uid= LlBH0JM0fzfanYUjbnN2wwuye6M2 , key=He7QKoyvOFLtIug7yufYpjKGh-vNd-8TKj7G5skay4gCNLqAlNCzlOG1f2bKihYe6UWVMnFiu4HRM2r4RbdI8g)


PIC_URL = “https://firebasestorage.googleapis.com/v0/b/chai-959f8-images/o/bots%2FLlBH0JM0fzfanYUjbnN2wwuye6M2_1646565687614_02d701fa-5f8d-472a-8fe9-b592af8166a8.jfif?alt=media&token=4da7f65c-c1bf-49c0-8e36-4d4047cae365”


package(
    Metadata(
        name=“Chenle”,
        image_url= https://firebasestorage.googleapis.com/v0/b/chai-959f8-images/o/bots%2FLlBH0JM0fzfanYUjbnN2wwuye6M2_1646565687614_02d701fa-5f8d-472a-8fe9-b592af8166a8.jfif?alt=media&token=4da7f65c-c1bf-49c0-8e36-4d4047cae365,
        color=“f1a2b3”,
        description=“Everyone are obviously weird”,
        input_class=Bot,
    )
)
uid = upload_and_deploy("_package.zip")
wait_for_deployment(uid)
share_bot(uid)
