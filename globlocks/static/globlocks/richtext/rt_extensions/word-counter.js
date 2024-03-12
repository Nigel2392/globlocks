const countSentences = (str) =>
    str ? (str.match(/[.?!…](\s|$)|\n+/g) || []).length : 0;

const countWords = (str) => 
    str ? str.split(/\s+/).length : 0;

const WordCounter = ({ getEditorState }) => {
    const editorState = getEditorState();
    const content = editorState.getCurrentContent();
    const text = content.getPlainText();

    const sentenceCount = countSentences(text);
    const wordCount = countWords(text);
    const charCount = text.length;
    const averageWordsPerSentence = Math.round(sentenceCount ? wordCount / sentenceCount : 0);
    const averageCharsPerWord = Math.round(wordCount ? charCount / wordCount : 0);

    let sentenceCountElem = window.React.createElement('div', {
        className: 'w-inline-block w-tabular-nums w-help-text w-mr-4',
    }, `S: ${sentenceCount}`);

    let wordCountElem = window.React.createElement('div', {
        className: 'w-inline-block w-tabular-nums w-help-text w-mr-4',
    }, `W: ${wordCount}`);

    let charCountElem = window.React.createElement('div', {
        className: 'w-inline-block w-tabular-nums w-help-text w-mr-4',
    }, `C: ${charCount}`);

    let averageWordsPerSentenceElem = window.React.createElement('div', {
        className: 'w-inline-block w-tabular-nums w-help-text w-mr-4',
    }, `Avg W/S: ${averageWordsPerSentence}`);

    let averageCharsPerWordElem = window.React.createElement('div', {
        className: 'w-inline-block w-tabular-nums w-help-text w-mr-4',
    }, `Avg C/W: ${averageCharsPerWord}`);



    return window.React.createElement('div', {
        className: 'w-flex w-flex-wrap',
    }, [
        sentenceCountElem,
        wordCountElem,
        charCountElem,
        averageWordsPerSentenceElem,
        averageCharsPerWordElem,
    ]);
}

window.draftail.registerPlugin({
    type: 'word-counter',
    meta: WordCounter,
}, 'controls');

