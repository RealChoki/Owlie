<template>
    <div class="d-flex justify-content-center container">
        <div class="d-flex flex-column justify-content-center align-items-center text-center vh-100 w-75">
            <h1 class="text-white fw-bold mb-4">
                Creating an AI Assistant that Empowers Independent Problem-Solving
            </h1>
            <p class="text-white w-75 paragraph-desktop">
                Welcome! We are a passionate team of 2 business informatics students 
                (<a href="https://github.com/RealChoki" class="text-white">Choki's GitHub</a> and 
                <a href="https://github.com/davidcraccer" class="text-white">David's GitHub</a>) from HTW Berlin with a dream.
                Meet Owlie – our innovative AI teaching assistant. Unlike traditional AI tools that often provide immediate answers, 
                Owlie encourages students to think critically and solve problems independently by offering hints, guidance, and personalized feedback.
            </p>
            <p class="text-white w-75 paragraph-desktop">
                Our goal is to address the challenges AI faces in education, such as promoting critical thinking over quick solutions, 
                and fostering a deeper understanding of concepts. By helping students develop problem-solving skills, we believe AI can truly empower learners.
            </p>
            <p class="text-white w-75 paragraph-mobile">
                We are two business informatics students (<a href="https://github.com/RealChoki" class="text-white">Choki</a> and 
                <a href="https://github.com/davidcraccer" class="text-white">David</a>) from HTW Berlin, passionate about AI in education.  
                Meet Owlie – an innovative AI teaching assistant designed to encourage critical thinking.  
                Instead of simply providing answers, Owlie offers hints, guidance, and personalized feedback to help students develop problem-solving skills  
                while maintaining academic integrity.
            </p>
            <img class="w-25 mt-4" src="../assets/icons/OwlLogo.png" alt="Owl Logo">
        </div>
    </div>
</template>

<style scoped>
.container{
  max-width: 1190px;
  min-width: 500px;
}


/* Hide long text on small screens */
.paragraph-mobile {
    display: none;
}

/* Show short text on small screens, hide long text */
@media (max-width: 768px) {
    .paragraph-desktop {
        display: none;
    }
    .paragraph-mobile {
        display: block;
    }
}
</style>
