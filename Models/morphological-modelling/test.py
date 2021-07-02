from morphological_analysis.morphological_modelling import Morphology

morph = Morphology()
print(morph.word_morphology('اليوم', 'noun'))
print(morph.word_morphology('شربكم', 'noun'))
print(morph.word_morphology('المظلومون', 'noun'))
print(morph.word_morphology('مدرستهم', 'noun'))
print(morph.word_morphology('فاسقيناكموه', 'verb'))