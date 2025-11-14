import json
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableSequence

try:
    from app.config import config
    OPENAI_MODEL = config.OPENAI_MODEL
except ImportError:
    OPENAI_MODEL = "gpt-4o-mini"


class FeedbackAgents:
    """Multi-agent system for comprehensive writing feedback."""

    def __init__(self, model: str = None, temperature: float = 0.2):
        self.model = model or OPENAI_MODEL
        self.llm = ChatOpenAI(model=self.model, temperature=temperature)
        self._setup_prompts()
        self._setup_chains()

    def _setup_prompts(self):
        """Setup prompt templates for all agents."""
        self.content_prompt = PromptTemplate(
            input_variables=['text', 'context'],
            template=(
                "You are ContentAnalysisAgent. Analyze the student's writing based on the reference context provided.\n\n"
                "Evaluate:\n"
                "1. Content accuracy and relevance\n"
                "2. Understanding of key concepts\n"
                "3. Completeness and originality\n"
                "4. Critical thinking\n"
                "5. Use of examples\n\n"
                "Reference Context:\n{context}\n\nStudent Writing:\n{text}\n\n"
                "Return JSON with keys: content_score, strengths, weaknesses, missing_concepts, suggestions"
            )
        )

        self.grammar_prompt = PromptTemplate(
            input_variables=['text'],
            template=(
                "You are GrammarAgent. Detect grammar mistakes.\n"
                "Return JSON with grammar_score, errors (line, type, issue, suggestion), overall_comment.\n\nText:\n{text}"
            )
        )

        self.vocab_prompt = PromptTemplate(
            input_variables=['text', 'jlpt_level'],
            template=(
                "You are VocabularyAgent. Evaluate vocabulary for JLPT level {jlpt_level}.\n"
                "Return JSON with vocab_score, vocab_comments, suggestions, advanced_words_used, simple_words.\n\nText:\n{text}"
            )
        )

        self.structure_prompt = PromptTemplate(
            input_variables=['text'],
            template=(
                "You are StructureAgent. Evaluate structure and organization.\n"
                "Return JSON with structure_score, has_intro, has_body, has_conclusion, suggestions, paragraph_feedback.\n\nText:\n{text}"
            )
        )

        self.fluency_prompt = PromptTemplate(
            input_variables=['text'],
            template=(
                "You are FluencyAgent. Evaluate fluency and naturalness.\n"
                "Return JSON with fluency_score, awkward_sentences, rewrites, overall_comment.\n\nText:\n{text}"
            )
        )

        self.scoring_prompt = PromptTemplate(
            input_variables=['analysis_json'],
            template=(
                "You are ScoringAgent. Calculate final score using:\n"
                "Content 30%, Grammar 25%, Vocabulary 20%, Structure 15%, Fluency 10%.\n"
                "Return JSON with overall_score, breakdown, grade_letter.\n\nAnalysis:\n{analysis_json}"
            )
        )

        self.feedback_prompt = PromptTemplate(
            input_variables=['text', 'analysis_json', 'overall_score', 'context'],
            template=(
                "You are FeedbackAgent. Create a comprehensive, encouraging feedback message.\n"
                "Return JSON with feedback_text, action_plan, practice_exercises, encouragement.\n\n"
                "Reference Context:\n{context}\n\nStudent Text:\n{text}\n\nAnalysis:\n{analysis_json}\n\nOverall Score: {overall_score}/10"
            )
        )

    def _setup_chains(self):
        """Create modern runnable pipelines (LangChain v1.x style)."""
        def make_chain(prompt: PromptTemplate):
            return RunnableSequence(prompt | self.llm)

        self.content_chain = make_chain(self.content_prompt)
        self.grammar_chain = make_chain(self.grammar_prompt)
        self.vocab_chain = make_chain(self.vocab_prompt)
        self.structure_chain = make_chain(self.structure_prompt)
        self.fluency_chain = make_chain(self.fluency_prompt)
        self.scoring_chain = make_chain(self.scoring_prompt)
        self.feedback_chain = make_chain(self.feedback_prompt)

    def _safe_parse(self, raw: str) -> Dict:
        try:
            if '```json' in raw:
                raw = raw.split('```json')[1].split('```')[0]
            elif '```' in raw:
                raw = raw.split('```')[1].split('```')[0]
            return json.loads(raw.strip())
        except Exception as e:
            print(f"JSON parse error: {e}")
            return {"raw": raw, "parse_error": str(e)}

    def run_multi_agents(self, text: str, context: str = "", jlpt_level: str = 'N5') -> Dict:
        results = {}

        # 1. Content
        if context:
            print("Running ContentAnalysisAgent...")
            results['content'] = self._safe_parse(self.content_chain.invoke({"text": text, "context": context}).content)
        else:
            results['content'] = {'content_score': 8, 'note': 'No reference context provided'}

        # 2. Grammar
        print("Running GrammarAgent...")
        results['grammar'] = self._safe_parse(self.grammar_chain.invoke({"text": text}).content)

        # 3. Vocabulary
        print("Running VocabularyAgent...")
        results['vocabulary'] = self._safe_parse(self.vocab_chain.invoke({"text": text, "jlpt_level": jlpt_level}).content)

        # 4. Structure
        print("Running StructureAgent...")
        results['structure'] = self._safe_parse(self.structure_chain.invoke({"text": text}).content)

        # 5. Fluency
        print("Running FluencyAgent...")
        results['fluency'] = self._safe_parse(self.fluency_chain.invoke({"text": text}).content)

        # 6. Scoring
        print("Running ScoringAgent...")
        analysis_json = json.dumps(results, ensure_ascii=False, indent=2)
        scoring_output = self.scoring_chain.invoke({"analysis_json": analysis_json}).content
        scoring_result = self._safe_parse(scoring_output)
        results['scoring'] = scoring_result
        results['overall_score'] = scoring_result.get("overall_score", 0)

        # 7. Feedback
        print("Running FeedbackAgent...")
        feedback_output = self.feedback_chain.invoke({
            "text": text,
            "analysis_json": analysis_json,
            "overall_score": results["overall_score"],
            "context": context or "No reference context available"
        }).content
        results['feedback'] = self._safe_parse(feedback_output)

        return results

    def generate_quick_feedback(self, text: str, jlpt_level: str = 'N5') -> str:
        """Short encouraging feedback."""
        quick_prompt = PromptTemplate(
            input_variables=['text', 'level'],
            template="Provide quick feedback (3-4 sentences) for {level} level writing.\nText:\n{text}"
        )
        chain = RunnableSequence(quick_prompt | self.llm)
        return chain.invoke({"text": text, "level": jlpt_level}).content


# Convenience wrappers
_default_agents = None

def get_feedback_agents(model: str = None) -> FeedbackAgents:
    global _default_agents
    if _default_agents is None:
        _default_agents = FeedbackAgents(model=model)
    return _default_agents

def run_multi_agents(text: str, context: str = "", jlpt_level: str = 'N5') -> Dict:
    agents = get_feedback_agents()
    return agents.run_multi_agents(text, context, jlpt_level)
