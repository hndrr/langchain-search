import { AnswerMessage } from "@/components/AnswerMessage";
import { QuestionMessage } from "@/components/QuestionMessage";
import { SearchMessage } from "@/components/SearchMessage";
import { SourceMessage } from "@/components/SourceMessage";

export default function Home() {
  return (
    <div className="font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col items-center">
        <div className="flex-1">
          <QuestionMessage content="Dummy Question" />
          <SearchMessage content="Dummy Search Message" />
          <SourceMessage sources={["https://example.com"]} />
          <AnswerMessage content="Dummy Answer Message" />
        </div>
        <form>
          <input
            className="rounded-lg border-2 border-gray-300 p-2"
            name="message"
            placeholder="テキストを入力"
            type="text"
          />
        </form>
      </main>
    </div>
  );
}
